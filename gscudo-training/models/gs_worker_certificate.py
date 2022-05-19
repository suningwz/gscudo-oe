import logging  # pylint: disable=unused-import
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class GSWorkerCertificate(models.Model):
    _name = "gs_worker_certificate"
    _description = "Certificazioni"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Certificazione")
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

    gs_certificate_type_id = fields.Many2one(
        comodel_name="gs_certificate_type",
        string="Tipo certificazione",
    )
    type = fields.Selection(
        string="Tipo",
        selection=[
            ("C", "Certificato"),
            ("E", "Esigenza formativa"),
        ],
        default="E",
        required=True,
    )
    active = fields.Boolean(string="Attivo", default=True)
    note = fields.Char(string="Note")

    issue_date = fields.Date(string="Data attestato")
    issue_serial = fields.Char(string="Protocollo attestato")

    external_link = fields.Char(string="Link Esterno")
    passed = fields.Boolean(string="Superato", compute="_compute_passed", store=True)

    # TODO is_updateable should influence this
    @api.depends(
        "gs_worker_id.gs_worker_certificate_ids.issue_date",
        "gs_certificate_type_id",
        "issue_date",
    )
    def _compute_passed(self):
        for certificate in self:
            if certificate.type == "E":
                certificate.passed = False
                return
            certificate_dates = [
                c.issue_date
                for c in certificate.gs_worker_id.gs_worker_certificate_ids
                if c.gs_certificate_type_id.satisfies(
                    certificate.gs_certificate_type_id
                )
                and c.issue_date is not False
                and c.type == "C"
            ]
            if certificate_dates and certificate.issue_date is not False:
                certificate.passed = certificate.issue_date < max(certificate_dates)
            else:
                certificate.passed = False

    is_update = fields.Boolean(string="È un aggiornamento")

    expiration_date = fields.Date(
        string="Data scadenza",
        compute="_compute_expiration_date",
        index=True,
        store=True,
    )

    @api.depends("issue_date", "gs_certificate_type_id.validity_interval")
    def _compute_expiration_date(self):
        """
        Computes the expiration date of the certificate.

        La data di scandenza di un certificato è sempre data dalla data di conseguimento
        più l'intervallo di validità alla situazione legale attuale.
        """
        for record in self:
            if (
                record.issue_date is not False
                and record.gs_certificate_type_id is not False
            ):
                record.expiration_date = record.issue_date + relativedelta(
                    years=record.gs_certificate_type_id.validity_interval
                )

    # @api.constrains("issue_date", "expiration_date")
    # def _check_date(self):
    #     if self.expiration_date is not False:
    #         if self.expiration_date is not False:
    #             if self.issue_date > self.expiration_date:
    #                 raise ValidationError(
    #                     "La data di scadenza deve essere successiva a quella dell'attestato"
    #                 )

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

    # TODO add a planned action that recomputes state
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

    # FIXME test this stuff
    def recompute_state(self):
        """
        Recomputes the validity state of the certificates that are either near the
        expiration date, or about two months from it
        """

        def domain_date_between(field, date: datetime.date, delta: relativedelta):
            """
            docstring
            """
            domain = ["&"]
            datefrom = (date - delta).strftime("%Y-%m-%d")
            dateto = (date - delta).strftime("%Y-%m-%d")
            domain.extend(
                [
                    (field, ">=", datefrom),
                    (field, "<=", dateto),
                ]
            )
            return domain

        today = datetime.now().date()
        two_days = relativedelta(days=2)
        two_months = relativedelta(months=2)

        model = self.env["gs_worker_certificate"]
        self.env.add_to_compute(
            model._fields["state"],
            model.search(
                [
                    "|",
                    domain_date_between("expiration_date", today, two_days),
                    domain_date_between(
                        "expiration_date", today + two_months, two_days
                    ),
                ]
            ),
        )

    is_required = fields.Boolean(
        string="Richiesto", compute="_compute_is_required", store=True, index=True
    )

    @api.depends("gs_worker_id", "gs_certificate_type_id")
    def _compute_is_required(self):
        for certificate in self:
            active_jobs = [
                job
                for job in certificate.gs_worker_id.gs_worker_job_ids
                if job.end_date is False
            ]
            certificate.is_required = False
            for job in active_jobs:
                for req in job.gs_certificate_type_ids:
                    if certificate.gs_certificate_type_id.satisfies(req):
                        certificate.is_required = True
                        return

    sg_id = fields.Integer(string="ID SawGest")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento Sawgest")
    sg_synched_at = fields.Datetime(string="Data ultima Syncronizzazione sawgest")

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
        # domain=[("state", "in", ["expired", "expiring"])],
        domain=[
            "|",
            ("state", "=", "expiring"),
            [
                ("state", "=", "expired"),
                ("is_required", "=", True),
            ],
        ],
    )

    # TODO performances
    def has_expiring_certificates(self):
        """
        Returns whether the worker has expiring certificates.
        """
        for worker in self:
            for certificate in worker.gs_worker_certificate_ids:
                if certificate.state == "expiring":
                    return True
        return False

    def has_expired_certificates(self):
        """
        Returns whether the worker has expired certificates that are required.
        """
        for worker in self:
            for certificate in worker.gs_worker_certificate_ids:
                if certificate.state == "expired" and certificate.is_required:
                    return True
        return False

    def has_expiring_unreq_certificates(self):
        """
        Returns whether the worker has expired certificates that are NOT required
        """
        for worker in self:
            for certificate in worker.gs_worker_certificate_ids:
                if certificate.state == "expired" and not certificate.is_required:
                    return True
        return False

    is_attentionable = fields.Boolean(
        string="Attenzionabile", compute="_compute_is_attentionable", store=True
    )

    @api.depends(
        "gs_worker_certificate_ids.state",
        "gs_worker_certificate_ids.is_required",
    )
    def _compute_is_attentionable(self):
        """
        Returns whether any of the above functions return true.
        """
        for worker in self:
            worker.is_attentionable = (
                len(worker.gs_worker_certificate_attentionable_ids) > 0
            )

    def action_recompute_is_attentionable(self):
        """
        Recompute the is_attentionable field for all workers.
        """
        model = self.env["gs_worker"]
        self.env.add_to_compute(model._fields["is_attentionable"], model.search([]))
