import logging  # pylint: disable=unused-import
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class GSWorkerCertificate(models.Model):
    _name = "gs_worker_certificate"
    _description = "Certificazioni"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # TODO cert name
    name = fields.Char(string="Certificazione", compute="_compute_name", store=True)

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
                f"{certificate.issue_date}"
            )

    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", index=True
    )
    contract_partner_id = fields.Many2one(
        related="gs_worker_id.contract_partner_id",
        comodel_name="res.partner",
        string="Azienda/Sede",
        store=True,
        index=True,
    )

    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Tipo certificazione",
    )

    type = fields.Selection(
        string="Tipo",
        selection=[
            ("C", "Certificato"),
            ("E", "Esigenza formativa"),
        ],
        default="C",
        required=True,
    )

    note = fields.Char(string="Note")

    issue_date = fields.Date(string="Data attestato")
    issue_serial = fields.Char(string="Protocollo attestato", store=True)

    @api.model
    def create(self, vals):
        """
        When a certificate is created, automatically set the issue number.
        """
        certificate = super().create(vals)
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
            if certificate.type == "E":
                certificate.active = True
                return
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

    is_update = fields.Boolean(string="Aggiornabile")

    expiry_date = fields.Date(string="Data scadenza (sawgest)")

    expiration_date = fields.Date(
        string="Data scadenza",
        compute="_compute_expiration_date",
        index=True,
        store=True,
    )

    @api.depends("issue_date", "gs_training_certificate_type_id.validity_interval")
    def _compute_expiration_date(self):
        """
        Computes the expiration date of the certificate.

        La data di scandenza di un certificato è sempre data dalla data di conseguimento
        più l'intervallo di validità alla situazione legale attuale.
        """
        for record in self:
            if (
                record.issue_date is not False
                and record.gs_training_certificate_type_id is not False
            ):
                record.expiration_date = record.issue_date + relativedelta(
                    years=record.gs_training_certificate_type_id.validity_interval
                )

    note = fields.Char(string="Note")

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
            if certificate.expiration_date is not False:
                if certificate.expiration_date < today:
                    certificate.state = "expired"
                elif certificate.expiration_date < today + relativedelta(months=2):
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

        def domain_date_between(field: str, date: datetime.date, delta: relativedelta):
            """
            Generates a search domain constraining the given field
            between date - delta and date + delta.
            """
            domain = ["&"]
            datefrom = (date - delta).strftime("%Y-%m-%d")
            dateto = (date + delta).strftime("%Y-%m-%d")
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
        comodel_name="gs_lesson_enrollment", string="Iscrizione al test"
    )

    duration = fields.Float(string="Durata", related="test_id.gs_course_id.duration")
    min_attendance = fields.Float(
        string="Partecipazione minima", related="test_id.gs_course_id.min_attendance"
    )
    attended_hours = fields.Float(string="Ore frequentate")
    attendance_percentage = fields.Float(
        string="Frequenza", compute="_compute_attendance_percentage"
    )

    @api.depends("attended_hours", "duration")
    def _compute_attendance_percentage(self):
        self.attendance_percentage = self.attended_hours / self.duration

    def compute_enrollments(self):
        """
        Compute the list of lesson enrollments that satisfies this certificate's requirements.
        """
        self.ensure_one()
        enrollments = []
        prev = self.test_id
        while prev.id is not False:
            enrollments.append(prev)
            prev = prev.previous_enrollment_id

        return reversed(enrollments)

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
                    # record.sg_url = base_url + "training_timetables/{}".format(
                    #     record.sg_id
                    # )
                else:
                    record.sg_url = False


class GSWorker(models.Model):
    _inherit = "gs_worker"

    gs_worker_certificate_ids = fields.One2many(
        comodel_name="gs_worker_certificate",
        inverse_name="gs_worker_id",
        string="Attestati",
        groups="gscudo-training.group_training_backoffice",
    )

    gs_worker_certificate_attentionable_ids = fields.One2many(
        comodel_name="gs_worker_certificate",
        inverse_name="gs_worker_id",
        string="Attestati attenzionabili",
        groups="gscudo-training.group_training_backoffice",
        domain=[
            ("active", "=", True),
            "|",
            ("state", "=", "expiring"),
            "&",
            ("state", "=", "expired"),
            ("is_required", "=", True),
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
            )
