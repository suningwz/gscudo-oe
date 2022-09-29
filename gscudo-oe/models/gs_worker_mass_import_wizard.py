import logging
from datetime import date, datetime, timedelta
from base64 import b64decode

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

try:
    import pandas as pd
except (ImportError, IOError) as err:
    _logger.debug(err)
    raise


NEEDED_KEYS = (
    "nome",
    "cognome",
    "codice_fiscale",
    "mansione",
    "data_assunzione",
    "sesso",
    "data_nascita",
    "comune_nascita",
)

OPTIONAL_KEYS = (
    "provincia_nascita",
    "telefono",
    "email",
)


class GSWorkerMassImportWizard(models.TransientModel):
    _name = "gs_worker_mass_import_wizard"
    _description = "Wizard importazione di massa anagrafiche"

    data = fields.Binary(string="File dipendenti")

    partner_id = fields.Many2one(comodel_name="res.partner", string="Azienda")

    @staticmethod
    def parse_file(data):
        """
        Returns a list with the parsed lines of the excel file
        and a list with parsing errors.

        Raises ValueError if there are missing columns.
        """

        df = pd.read_excel(data, header=1, skipfooter=1)
        df = df.rename(columns=lambda x: x.strip())
        df = df.dropna(how="all")

        if not set(NEEDED_KEYS + OPTIONAL_KEYS).issubset(set(df)):
            raise ValueError("colonne mancanti")

        if not pd.core.dtypes.common.is_datetime64_dtype(df["data_assunzione"]):
            raise ValueError("data_assunzione contiene oggetti non data")

        if not pd.core.dtypes.common.is_datetime64_dtype(df["data_nascita"]):
            raise ValueError("data_nascita contiene oggetti non data")

        df_obj = df.select_dtypes(["object"])
        df[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

        df["sesso"] = df["sesso"].str.upper()
        df["codice_fiscale"] = df["codice_fiscale"].str.upper()

        parsed = []
        non_parsed = []

        for _, line in df.iterrows():
            line_errors = []

            for key in NEEDED_KEYS:
                # empty strings?
                if line.isna()[key]:
                    line_errors.append(f"{key} mancante")

            if line["sesso"] not in ("M", "F"):
                line_errors.append("errore sesso")

            if (
                line.notna()["data_nascita"]
                and line.notna()["data_assunzione"]
                and line["data_nascita"].date() + timedelta(days=365 * 10)
                > line["data_assunzione"].date()
            ):
                line_errors.append("data di nascita e data di assunzione troppo vicine")

            # TODO check fiscal code

            if line_errors:
                non_parsed.append((dict(line), line_errors))
            else:
                parsed.append(dict(line))

        return (parsed, non_parsed)

    @api.model
    def update_chatter(self, res_model, res_id, body, datas):
        """Adds the import data in the chatter, and attaches the import file."""
        attachment = self.env["ir.attachment"].create(
            {
                "name": f"Importazione anagrafiche lavoratori {date.today()}",
                "type": "binary",
                "datas": datas,
                "mimetype": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            }
        )

        res = self.env[res_model].search([("id", "=", res_id)])
        if not res:
            raise UserError("Can't update the chatter.")

        res.message_post(body=body, attachment_ids=[attachment.id])

    # pylint: disable-next
    def import_workers(self):
        """Reads the supplied file and creates the workers."""
        try:
            lines, errors = self.parse_file(b64decode(self.data))
        except ValueError as e:
            raise UserError(f"File malformato: {e}") from e

        worker_model = self.env["gs_worker"]
        contract_model = self.env["gs_worker_contract"]
        job_model = self.env["gs_worker_job"]

        for line in lines[:]:
            is_wrong = False

            worker = worker_model.search([("fiscalcode", "=", line["codice_fiscale"])])

            worker_data = {
                "firstname": line["nome"],
                "surname": line["cognome"],
                "fiscalcode": line["codice_fiscale"],
                "sex": line["sesso"],
                "birth_date": line["data_nascita"],
                "email": line["email"],
                "birth_place": (
                    # fmt: off
                    f"{line['comune_nascita']}" +
                    (
                        f" ({line['provincia_nascita']})"
                        if line["provincia_nascita"] not in (False, "EE")
                        else ""
                    )
                    # fmt: on
                ),
                "phone_number": line["telefono"],
            }

            if not worker:
                worker = worker_model.create(worker_data)
            else:
                worker.write(worker_data)

            current_contract = None
            # if there are multiple open contracts with the selected partner
            # chose one at random as current
            for contract in worker.gs_worker_contract_ids:
                if (
                    contract.partner_id == self.partner_id
                    and contract.end_date is False
                ):
                    current_contract = contract
                    continue

                if contract.start_date >= line["data_assunzione"].date():
                    is_wrong = True
                    errors.append(
                        (line, ["contratto aperto in data successiva presente"])
                    )
                    break

            if is_wrong:
                lines.remove(line)
                continue

            contract_data = {
                "gs_worker_id": worker.id,
                "partner_id": self.partner_id.id,
                "start_date": line["data_assunzione"].date(),
                "job_description": line["mansione"],
            }
            try:
                if current_contract is None:
                    current_contract = contract_model.create(contract_data)
                else:
                    current_contract.write(contract_data)
            except ValidationError as e:
                e = str(e)
                error_data = e if len(e.split(": ")) == 1 else e.split(": ")[1]
                errors.append((line, [error_data]))
                lines.remove(line)
                continue

            for contract in worker.gs_worker_contract_ids:
                if contract != current_contract and contract.end_date is False:
                    contract.end_date = line["data_assunzione"].date() - timedelta(
                        days=1
                    )
                    note = f"Chiuso da importazione {self.partner_id.name} del {datetime.today()}"
                    contract.note = (
                        " ".join((contract.note, note))
                        if contract.note is not False
                        else note
                    )

            worker.gs_worker_contract_id = current_contract.id

            current_job = None
            for job in worker.gs_worker_job_ids:
                if job.gs_worker_contract_id == current_contract:
                    current_job = job
                    continue

                if (
                    job.end_date is False
                    and job.gs_worker_contract_id.end_date is not False
                ):
                    job.end_date = job.gs_worker_contract_id.end_date

            job_data = {
                "gs_worker_contract_id": current_contract.id,
                "start_date": line["data_assunzione"].date(),
                "job_description": line["mansione"],
            }
            if current_job is None:
                current_job = job_model.create(job_data)
            else:
                current_job.write(job_data)

        # pylint: disable-next=no-else-return
        if errors:
            text = (
                f"<p>{len(lines)} lavoratori importati</p>"
                f"<p>{len(errors)} lavoratori non importati:"
            )

            text += (
                "<ul>"
                + "".join(
                    f"<li><b>{e[0]['nome']} {e[0]['cognome']} ({e[0]['codice_fiscale']}) </b>: "
                    + "<ul>"
                    + "".join(f"<li>{x}</li>" for x in e[1])
                    + "</ul></li>"
                    for e in errors
                )
                + "</ul></p>"
            )

        else:
            text = f"<p>{len(lines)} lavoratori importati</p>"

        self.update_chatter(
            res_model="res.partner",
            res_id=self.partner_id.id,
            body=text,
            datas=self.data,
        )

        return self.env["gs_message_wizard"].display_message(
            title="Attenzione" if errors else "Ok",
            message=text,
        )
