import csv
from datetime import datetime, timedelta
from base64 import b64decode

from odoo import models, fields
from odoo.exceptions import UserError

NEEDED_KEYS = (
    "nome",
    "cognome",
    "codice_fiscale",
    "mansione",
    "data_assunzione",
    "sesso",
    "data_nascita",
    "comune_nascita",
    "email",
)

OPTIONAL_KEYS = (
    "provincia_nascita",
    "telefono",
)


class DIALECT(csv.excel):
    """Describes the right properties of the excel-generated csv file."""

    delimiter = ";"


class GSWorkerMassImportWizard(models.TransientModel):
    _name = "gs_worker_mass_import_wizard"
    _description = "Wizard importazione di massa anagrafiche"

    csv_data = fields.Binary(string="File dipendenti")

    partner_id = fields.Many2one(comodel_name="res.partner", string="Azienda")

    @staticmethod
    def parse_csv(data):
        """
        Returns a list with the parsed lines of the csv
        and a list with parsing errors.

        Raises ValueError if there are missing columns.
        """

        lines = list(csv.DictReader(data.split("\n"), dialect=DIALECT))

        parsed = []
        non_parsed = []

        for i, line in enumerate(lines):
            i += 1
            line_errors = []

            line = {k: v.strip() for k, v in line.items()}

            if not set(NEEDED_KEYS + OPTIONAL_KEYS).issubset(line.keys()):
                raise ValueError("colonne mancanti")

            for key in line:
                if line[key] == "":
                    line[key] = False
                    if key in NEEDED_KEYS:
                        line_errors.append(f"{key} mancante")
                        continue

                if key in ("data_nascita", "data_assunzione"):
                    try:
                        line[key] = datetime.strptime(line[key], "%d/%m/%Y")
                    except ValueError:
                        line_errors.append(f"errore {key}")
                    continue

                if key == "sesso":
                    line[key] = line[key].upper()
                    if line[key] not in ("M", "F"):
                        line_errors.append(f"errore {key}")

                if key == "codice_fiscale":
                    line[key] = line[key].upper()

            if (
                line["data_nascita"] is not False
                and line["data_assunzione"] is not False
                and line["data_nascita"] + timedelta(days=365 * 10)
                > line["data_assunzione"]
            ):
                line_errors.append("data di nascita e data di assunzione troppo vicine")

            # TODO check fiscal code

            if line_errors:
                non_parsed.append((line, line_errors))
            else:
                parsed.append(line)

        return (parsed, non_parsed)

    def import_workers(self):
        """Reads the supplied file and creates the workers."""
        try:
            data = b64decode(self.csv_data).decode("utf-8")
            lines, errors = self.parse_csv(data)
        except ValueError as e:
            raise UserError("Impossibile importare il file:\n" + "\n".join(e)) from e

        # TODO manage errors

        worker_model = self.env["gs_worker"]
        contract_model = self.env["gs_worker_contract"]
        job_model = self.env["gs_worker_job"]

        for line in lines:
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
                # TODO check this
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

                if contract.start_date > line["data_assunzione"]:
                    is_wrong = True
                    errors.append((line, ["discrepanza date contratti"]))
                    break

            if is_wrong:
                continue

            contract_data = {
                "gs_worker_id": worker.id,
                "partner_id": self.partner_id.id,
                "start_date": line["data_assunzione"],
                "job_description": line["mansione"],
            }
            if current_contract is None:
                current_contract = contract_model.create(contract_data)
            else:
                current_contract.write(contract_data)

            for contract in worker.gs_worker_contract_ids:
                if contract != current_contract and contract.end_date is False:
                    contract.end_date = line["data_assunzione"] - timedelta(days=1)
                    contract.note = " ".join(
                        (
                            contract.note,
                            f"Chiuso da importazione {self.partner_id.name} del {datetime.today()}",
                        )
                    )

            worker.gs_worker_contract_id = current_contract.id

            current_job = None
            # TODO ???
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
                "start_date": line["data_assunzione"],
                "job_description": line["mansione"],
            }
            if current_job is None:
                current_job = job_model.create(job_data)
            else:
                current_job.write(job_data)

        if errors:
            text = (
                f"{len(lines)} lavoratori importati\n\n"
                f"{len(errors)} lavoratori non importati:\n"
            )

            text += "\n".join(
                f"{e[0]['nome']} {e[0]['cognome']} {e[0]['codice_fiscale']} - "
                f"{','.join(e[1])}"
                for e in errors
            )

            message = self.env["gs_message_wizard"].create({"message": text})

            return {
                "name": "Attenzione",
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "gs_message_wizard",
                "res_id": message.id,
                "target": "new",
            }

        else:
            message = self.env["gs_message_wizard"].create(
                {"message": f"{len(lines)} lavoratori importati"}
            )

            return {
                "name": "Ok",
                "type": "ir.actions.act_window",
                "view_mode": "form",
                "res_model": "gs_message_wizard",
                "res_id": message.id,
                "target": "new",
            }
            # raise UserError(errors)
