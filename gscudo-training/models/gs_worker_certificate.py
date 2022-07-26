import base64
import logging  # pylint: disable=unused-import
import datetime
from datetime import datetime
from tempfile import NamedTemporaryFile
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    from docxtpl import DocxTemplate
    from jinja2.exceptions import UndefinedError
except (ImportError, IOError) as err:
    _logger.error(err)


class GSWorkerCertificate(models.Model):
    _name = "gs_worker_certificate"
    _description = "Certificazioni"
    _inherit = ["mail.thread", "mail.activity.mixin", "documents.mixin"]

    def _get_document_folder(self):
        return self.env["documents.folder"].search([("name", "=", "Formazione")])

    def _get_document_tags(self):
        return self.env["documents.tag"].search([("name", "=", "Attestato")])

    name = fields.Char(
        string="Certificazione", compute="_compute_name", store=True, tracking=True
    )

    @api.depends(
        "gs_worker_id.name",
        "gs_training_certificate_type_id.name",
        "issue_date",
    )
    def _compute_name(self):
        for certificate in self:
            certificate.name = (
                f"{certificate.gs_worker_id.name} - "
                f"{certificate.gs_training_certificate_type_id.name} - "
                f"{certificate.issue_date if certificate.type == 'C' else 'ESIGENZA'}"
            )

    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", index=True, tracking=True
    )
    contract_partner_id = fields.Many2one(
        related="gs_worker_id.contract_partner_id",
        comodel_name="res.partner",
        string="Azienda/Sede",
        store=True,
        index=True,
        tracking=True,
    )

    has_training_manager = fields.Boolean(
        string="Manager Formativo",
        related="gs_worker_id.contract_partner_id.has_training_manager",
    )

    has_safety = fields.Boolean(
        string="RSPP/Supporto RSPP",
        related="gs_worker_id.contract_partner_id.has_safety",
    )

    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Tipo certificazione",
        tracking=True,
    )

    type = fields.Selection(
        string="Tipo",
        selection=[
            ("C", "Certificato"),
            ("E", "Esigenza formativa"),
        ],
        default="C",
        required=True,
        tracking=True,
        index=True,
    )

    note = fields.Char(string="Note")

    issue_date = fields.Date(string="Data certificato", tracking=True, index=True)
    issue_serial = fields.Char(
        string="Protocollo certificato", store=True, tracking=True, index=True
    )

    @api.model
    def create(self, vals):
        """
        When a certificate is created, automatically set the issue number.
        Also, if this is a multicertificate, set the appropriate certificate type.
        """
        if "gs_training_certificate_type_id" in vals:
            certificate_type = self.env["gs_training_certificate_type"].browse(
                [vals["gs_training_certificate_type_id"]]
            )
            certificate_type.ensure_one()

            # FIXME look at training need
            if certificate_type.is_multicert:
                domain_tail = []
                for implied_cert in certificate_type.weaker_certificate_ids:
                    domain_tail.append(
                        (
                            "gs_training_certificate_type_id",
                            "=",
                            implied_cert.id,
                        )
                    )
                domain = [("gs_worker_id", "=", vals["gs_worker_id"])]
                domain.extend(["|" for _ in range(len(domain_tail) - 1)])
                domain.extend(domain_tail)

                certificate_to_update = self.env["gs_worker_certificate"].search(
                    domain, limit=1, order="issue_date desc"
                )

                # For now keep the multicertificate
                if not certificate_to_update:
                    certificate = super().create(vals)
                    if certificate.type == "C":
                        certificate.issue_serial = f"CERT-{certificate.id}"
                    return certificate

                    # worker = self.env["gs_worker"].browse([vals["gs_worker_id"]])
                    # worker.ensure_one()
                    # raise UserError(
                    #     f"{worker.fiscalcode} non può aggiornare un certificato che non ha."
                    # )

                certificate_to_update.ensure_one()

                new_certificate_type = (
                    certificate_to_update.gs_training_certificate_type_id
                )

                # this is bad and fragile, but for now it is the only way we can do this
                if certificate_type.code == "ASR-P-AGG":
                    if self.env["gs_worker_certificate"].search(
                        [
                            ("gs_worker_id", "=", vals["gs_worker_id"]),
                            ("gs_training_certificate_type_id.code", "=", "ASR-PR"),
                        ]
                    ):
                        pr_type = self.env["gs_training_certificate_type"].search(
                            [("code", "=", "ASR-PR")]
                        )
                        pr_type.ensure_one()

                        pr_vals = vals.copy()
                        pr_vals["gs_training_certificate_type_id"] = pr_type.id
                        self.env["gs_worker_certificate"].create(pr_vals)

                vals["gs_training_certificate_type_id"] = new_certificate_type.id

        certificate = super().create(vals)
        if certificate.type == "C":
            certificate.issue_serial = f"CERT-{certificate.id}"
        return certificate

    external_link = fields.Char(string="Link Esterno")

    active = fields.Boolean(string="Attivo", compute="_compute_active", store=True)

    @api.depends(
        "gs_worker_id.gs_worker_certificate_ids.issue_date",
        "gs_training_certificate_type_id",
        "issue_date",
    )
    def _compute_active(self):
        """
        Here active means that there is not a newer certificate of the same type
        or greater.
        It's the opposite of the old "passed" field.
        """
        for certificate in self:
            # if certificate.type == "E":
            #     certificate.active = True
            #     return
            certificate_dates = [
                c.issue_date
                for c in certificate.gs_worker_id.gs_worker_certificate_ids
                if (
                    c.gs_training_certificate_type_id
                    in certificate.gs_training_certificate_type_id.weaker_certificates()
                )
                and c.issue_date is not False
                and c.type == "C"
            ]
            if certificate_dates and certificate.issue_date is not False:
                # a certificate is active if its date is the biggest among the
                # certificates of the same type
                certificate.active = certificate.issue_date == max(certificate_dates)
            else:
                certificate.active = True

    is_update = fields.Boolean(string="Aggiornamento", tracking=True)

    expiry_date = fields.Date(string="Data scadenza (sawgest)")

    expiration_date = fields.Date(
        string="Data scadenza",
        compute="_compute_expiration_date",
        index=True,
        store=True,
        tracking=True,
    )

    @api.depends("issue_date", "gs_training_certificate_type_id.validity_interval")
    def _compute_expiration_date(self):
        """
        Computes the expiration date of the certificate.

        La data di scandenza di un certificato è sempre data dalla data di conseguimento
        più l'intervallo di validità alla situazione legale attuale.
        """
        for record in self:
            if record.type == "E":
                record.expiration_date = record.issue_date
            elif (
                record.issue_date is not False
                and record.gs_training_certificate_type_id is not False
            ):
                if record.gs_training_certificate_type_id.validity_interval != 0:
                    record.expiration_date = record.issue_date + relativedelta(
                        years=record.gs_training_certificate_type_id.validity_interval
                    )
                else:
                    # record.gs_training_certificate_type_id.validity_interval = 99
                    record.expiration_date = record.issue_date + relativedelta(years=99)

    state = fields.Selection(
        string="Validità",
        selection=[
            ("valid", "Valido"),
            ("expiring", "In scadenza"),
            ("expired", "Scaduto"),
            ("na", "Non disponibile"),
        ],
        compute="_compute_state",
        index=True,
        store=True,
    )

    @api.depends("expiration_date")
    def _compute_state(self):
        today = datetime.now().date()
        for certificate in self:
            if certificate.type == "E":
                certificate.state = "expired"
            elif certificate.expiration_date is not False:
                if certificate.expiration_date <= today:
                    certificate.state = "expired"
                elif certificate.expiration_date <= today + relativedelta(months=2):
                    certificate.state = "expiring"
                else:
                    certificate.state = "valid"
            else:
                certificate.state = "na"

    def recompute_state(self):
        """
        Recomputes the validity state of the certificates that are either near the
        expiration date, or about two months from it
        """

        def domain_date_between(
            field: str, base_date: datetime.date, delta: relativedelta
        ):
            """
            Generates a search domain constraining the given field
            between date - delta and date + delta.
            """
            domain = ["&"]
            datefrom = (base_date - delta).strftime("%Y-%m-%d")
            dateto = (base_date + delta).strftime("%Y-%m-%d")
            domain.extend([(field, ">=", datefrom), (field, "<=", dateto)])
            return domain

        # logging.info("Recomputing certificates state")

        today = datetime.now().date()
        two_days = relativedelta(days=2)
        two_months = relativedelta(months=2)

        domain = ["|"]
        domain.extend(domain_date_between("expiration_date", today, two_days))
        domain.extend(
            domain_date_between("expiration_date", today + two_months, two_days)
        )

        self.env.add_to_compute(
            self._fields["state"],
            self.search(domain),
        )

    is_required = fields.Boolean(
        string="Richiesto", compute="_compute_is_required", store=True, index=True
    )

    # LOW depends
    @api.depends("gs_worker_id", "gs_training_certificate_type_id")
    def _compute_is_required(self):
        for certificate in self:
            active_jobs = [
                job
                for job in certificate.gs_worker_id.gs_worker_job_ids
                if job.end_date is False
            ]
            certificate.is_required = False
            for job in active_jobs:
                for req in job.gs_training_certificate_type_ids:
                    if (
                        req
                        in certificate.gs_training_certificate_type_id.weaker_certificates()
                    ):
                        certificate.is_required = True
                        return

    test_id = fields.Many2one(
        comodel_name="gs_lesson_enrollment", string="Iscrizione al test", tracking=True
    )

    duration = fields.Float(
        string="Durata", related="test_id.gs_course_id.duration", tracking=True
    )
    min_attendance = fields.Float(
        string="Partecipazione minima",
        related="test_id.gs_course_id.min_attendance",
        tracking=True,
    )
    attended_hours = fields.Float(string="Ore frequentate", tracking=True)
    attendance_percentage = fields.Float(
        string="Frequenza", compute="_compute_attendance_percentage"
    )

    @api.depends("attended_hours", "duration")
    def _compute_attendance_percentage(self):
        self.attendance_percentage = (
            (self.attended_hours / self.duration) if self.duration > 0 else 1
        )

    enrollments = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        string="Lezioni seguite",
        compute="_compute_enrollment_field",
    )

    def _compute_enrollment_field(self):
        enrollments = [e.id for e in self.compute_enrollments()]
        self.enrollments = enrollments if enrollments else False

    def compute_enrollments(self):
        """
        Compute the list of lesson enrollments that satisfies this certificate's requirements.
        """
        self.ensure_one()
        enrollments = []
        prev = self.test_id
        while prev.id:
            enrollments.append(prev)
            prev = prev.previous_enrollment_id

        return list(reversed(enrollments))

    gs_course_enrollment_ids = fields.One2many(
        comodel_name="gs_course_enrollment",
        inverse_name="gs_worker_certificate_id",
        string="Iscrizioni rinnovo",
    )
    gs_course_enrollment_id = fields.Many2one(
        comodel_name="gs_course_enrollment",
        string="Iscrizione rinnovo",
        compute="_compute_gs_course_enrollment_id",
    )

    def _compute_gs_course_enrollment_id(self):
        for record in self:
            if record.gs_course_enrollment_ids:
                record.gs_course_enrollment_id = record.gs_course_enrollment_ids[0].id
            else:
                record.gs_course_enrollment_id = False

    is_renewed = fields.Boolean(string="Rinnovato", compute="_compute_is_renewed")

    def _compute_is_renewed(self):
        for record in self:
            record.is_renewed = bool(record.gs_course_enrollment_id)

    gs_possible_course_ids = fields.One2many(
        comodel_name="gs_course",
        string="Corsi possibili per rinnovo",
        compute="_compute_gs_possible_course_ids",
    )

    def _compute_gs_possible_course_ids(self):
        for record in self:
            record.gs_possible_course_ids = self.env["gs_course"].search(
                [
                    (
                        "gs_course_type_id.gs_training_certificate_type_id.id",
                        "=",
                        record.gs_training_certificate_type_id.id,
                    ),
                    ("start_date", ">", datetime.now().date()),
                ]
            )

    def enrollment_wizard(self):
        """
        Given one or more training needs, call the enrollment wizard
        on the selected worker(s) for courses of the right type.
        """
        cert_types = set(record.gs_training_certificate_type_id for record in self)
        if len(cert_types) != 1:
            raise UserError(
                "Tutte le esigenze devono essere per lo stesso tipo di certificato."
            )
        cert_type_id = cert_types.pop().id

        if any(
            requirement.gs_course_enrollment_ids.id is not False
            for requirement in cert_types
        ):
            raise UserError("Esigenza formativa già risolta")

        action = {
            "name": "Iscrivi a un corso...",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "gs_course_certificate_enrollment_wizard",
            "context": {
                "default_gs_training_certificate_type_id": cert_type_id,
                # "active_id": self.env.context.get("active_id"),
                "active_ids": self.env.context.get("active_ids"),
            },
        }

        return action

    sg_id = fields.Integer(string="ID SawGest")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento Sawgest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SawGest")

    sg_url = fields.Char(
        string="Vedi in sawgest", compute="_compute_sg_url", store=False
    )

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_id and record.sg_id > 0:
                    record.sg_url = f"{base_url}training_timetables/{record.sg_id}"
                else:
                    record.sg_url = False

    @api.model
    def generate_docs(self):
        """
        Mass document generation.
        """
        certificates = self.browse(self.env.context.get("active_ids"))
        for certificate in certificates:
            certificate.generate_doc()

    def generate_doc(self):
        """
        Generates a docx/pdf document for the certificate.
        """

        def hours(time: int) -> str:
            hours = int(time)
            mins = int((time - hours) * 60)
            return f"{hours}:{mins:02}"

        # FIXME partner name
        def address(partner) -> str:
            return f"{partner.street} {partner.zip} {partner.city} ({partner.state_id.code})"

        for certificate in self:
            if self.env["ir.attachment"].search(
                [
                    ("res_model", "=", "gs_worker_certificate"),
                    ("res_id", "=", certificate.id),
                ]
            ):
                continue

            doc_template = certificate.test_id.gs_course_id.document_template_id
            if not doc_template:
                raise UserError("Template mancante.")

            # select the data
            data = {
                "name": certificate.gs_worker_id.name,
                "birth_date": certificate.gs_worker_id.birth_date,
                # FIXME
                "birth_place": (
                    certificate.gs_worker_id.birth_place
                    if certificate.gs_worker_id.birth_place
                    else certificate.gs_worker_id.birth_country
                ),
                "fiscalcode": certificate.gs_worker_id.fiscalcode,
                "partner": certificate.gs_worker_id.contract_partner_id.name,
                "job_description": certificate.gs_worker_id.contract_job_description,
                "course_name": certificate.test_id.gs_course_id.gs_course_type_id.name,
                "law_ref": certificate.gs_training_certificate_type_id.law_ref,
                "duration": hours(certificate.test_id.gs_course_id.duration),
                "lessons": [
                    {
                        "date": e.gs_course_lesson_id.start_time.strftime("%d-%m-%Y"),
                        "location": address(e.gs_course_lesson_id.location_partner_id),
                        "duration": hours(e.gs_course_lesson_id.duration),
                        "teacher": e.gs_course_lesson_id.teacher_partner_id.name,
                        "coteacher": (
                            e.gs_course_lesson_id.coteacher_partner_id.name
                            if e.gs_course_lesson_id.coteacher_partner_id.name
                            is not False
                            else ""
                        ),
                    }
                    for e in certificate.compute_enrollments()
                    if not e.gs_course_lesson_id.generate_certificate
                ],
                "attended_hours": hours(certificate.attended_hours),
                "min_attendance": int(certificate.min_attendance * 100),
                "ateco": certificate.gs_worker_id.contract_partner_id.main_ateco_id.code,
                "issue_date": certificate.issue_date.strftime("%d/%m/%Y"),
                "issue_serial": certificate.issue_serial,
            }

            # pylint: disable-next=consider-using-dict-items
            for key in data:
                # FIXME custom check for lessons
                if data[key] is False:
                    raise UserError(
                        f"Missing parameter '{key}' for certificate {certificate.issue_serial}"
                    )

            # create the document
            with NamedTemporaryFile("w+b") as f:
                f.write(base64.b64decode(doc_template.template))
                document = DocxTemplate(f.name)

                try:
                    document.render(data)
                    document.save(f.name)
                except UndefinedError as e:
                    _logger.warning(e)
                    raise e

                # convert it in pdf

                # save it as an attachment
                f.seek(0)
                self.env["ir.attachment"].create(
                    {
                        "name": (
                            f"{certificate.gs_worker_id.fiscalcode} - "
                            f"{certificate.test_id.gs_course_id.protocol} - "
                            f"{certificate.issue_date}"
                            ".docx"
                        ),
                        "description": f"Generato il {datetime.now().date()}",
                        "res_model": "gs_worker_certificate",
                        "res_id": certificate.id,
                        "type": "binary",
                        "datas": base64.encodebytes(f.read()),
                        "mimetype": (
                            "application/vnd.openxmlformats-officedocument"
                            ".wordprocessingml.document"
                        ),
                    }
                )


class GSWorker(models.Model):
    _inherit = "gs_worker"

    gs_worker_certificate_ids = fields.One2many(
        comodel_name="gs_worker_certificate",
        inverse_name="gs_worker_id",
        string="Certificati",
        groups="gscudo-training.group_training_backoffice",
    )

    # FIXME attentionable filter on certificates view
    gs_worker_certificate_attentionable_ids = fields.One2many(
        comodel_name="gs_worker_certificate",
        inverse_name="gs_worker_id",
        string="Certificati attenzionabili",
        groups="gscudo-training.group_training_backoffice",
        domain=[
            ("active", "=", True),
            ("gs_course_enrollment_ids", "=", False),
            "|",
            "|",
            ("type", "=", "E"),
            ("state", "=", "expiring"),
            # "&",
            ("state", "=", "expired"),
            # ("is_required", "=", True),
        ],
    )

    is_attentionable = fields.Boolean(
        string="Attenzionabile", compute="_compute_is_attentionable", store=True
    )

    @api.depends(
        "gs_worker_certificate_ids.state",
        "gs_worker_certificate_ids.is_required",
    )
    def _compute_is_attentionable(self):
        for worker in self:
            worker.is_attentionable = (
                len(worker.gs_worker_certificate_attentionable_ids) > 0
                or len(worker.gs_worker_certificate_ids) == 0
            )
