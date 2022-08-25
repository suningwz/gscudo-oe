from datetime import datetime, timedelta, date
from odoo import api, fields, models
from odoo.exceptions import ValidationError

# from odoo.exceptions import UserError


class WorkerContract(models.Model):
    _name = "gs_worker_contract"
    _description = "Relazione Worker Partner"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome", compute="_compute_name", store=True)
    active = fields.Boolean(string="Attivo", default=True)
    note = fields.Char(string="Note")
    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", required=True, index=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Azienda/Sede", required=True, index=True
    )
    is_owner = fields.Boolean(string="È Titolare")
    is_dependent = fields.Boolean(string="È dipendente")
    employee_serial = fields.Char(string="Matricola dip.")
    start_date = fields.Date(string="Data inizio", required=True, tracking=True)
    end_date = fields.Date(string="Data fine", tracking=True)
    job_description = fields.Char(string="Mansione")
    department = fields.Char(string="Reparto/ufficio")
    sg_job_careers_id = fields.Integer(string="ID SaWGest")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima Sincronizzazione SaWGest")

    @api.depends("start_date", "end_date", "job_description", "partner_id")
    def _compute_name(self):
        for record in self:
            # pylint: disable-next=consider-using-f-string
            record.name = "{} {}".format(
                record.job_description or "**Impiegato**",
                # record.partner_id.name or "",
                (record.start_date or date.today()).strftime("%d/%m/%Y"),
            )

    @api.constrains("start_date", "end_date")
    def _check_date(self):
        if self.start_date is not False:
            if self.start_date < (datetime.now() - timedelta(days=70 * 365)).date():
                raise ValidationError(
                    f"Lavoratore {self.gs_worker_id.id}: "
                    "la data di inizio deve essere negli ultimi 70 anni"
                )
            if self.start_date > (datetime.now() + timedelta(days=30)).date():
                raise ValidationError(
                    f"Lavoratore {self.gs_worker_id.id}: "
                    "la data di inizio deve essere entro i prossimi 30 giorni"
                )
            if self.end_date is not False:
                if self.start_date > self.end_date:
                    raise ValidationError(
                        f"Lavoratore {self.gs_worker_id.id}: "
                        "la data di fine deve essere maggiore di quella di inizio"
                    )
                if self.end_date > (datetime.now() + timedelta(days=365)).date():
                    raise ValidationError(
                        f"Lavoratore {self.gs_worker_id.id}: "
                        "la data di fine deve essere entro i prossimi 365 giorni"
                    )


class GSWorker(models.Model):
    _inherit = "gs_worker"

    gs_worker_contract_id = fields.Many2one(
        comodel_name="gs_worker_contract",
        string="Impiego attuale",
        # domain="[('gs_worker_id'),'=',id]"
        index=True,
    )
    contract_partner_id = fields.Many2one(
        related="gs_worker_contract_id.partner_id",
        comodel_name="res.partner",
        string="Azienda/Sede",
        store=True,
        index=True,
    )
    contract_employee_serial = fields.Char(
        related="gs_worker_contract_id.employee_serial",
        string="Matricola dip.",
        store=True,
    )
    contract_is_owner = fields.Boolean(
        related="gs_worker_contract_id.is_owner", string="È Titolare", store=True
    )
    contract_is_dependent = fields.Boolean(
        related="gs_worker_contract_id.is_dependent", string="È Dipendente", store=True
    )
    contract_start_date = fields.Date(
        related="gs_worker_contract_id.start_date", string="Data inizio", store=True
    )
    contract_end_date = fields.Date(
        related="gs_worker_contract_id.end_date", string="Data fine", store=True
    )
    contract_job_description = fields.Char(
        related="gs_worker_contract_id.job_description", string="Mansione", store=True
    )
    contract_department = fields.Char(
        related="gs_worker_contract_id.department", string="Reparto/ufficio", store=True
    )

    gs_worker_contract_ids = fields.One2many(
        comodel_name="gs_worker_contract",
        inverse_name="gs_worker_id",
        string="Contratti/Posizioni",
    )

    @api.model
    def detach_worker_expired_contract(self):
        """Stacca i contratti Scaduti"""
        workers = self.env["gs_worker"].search(
            [("contract_end_date", "<", datetime.now())]
        )
        for worker in workers:
            worker.gs_worker_contract_id = False


class ResPartner(models.Model):
    _inherit = "res.partner"

    gs_worker_ids = fields.One2many(
        comodel_name="gs_worker",
        inverse_name="contract_partner_id",
        string="Lavoratori",
    )

    workers_count = fields.Integer(
        string="N. Lavoratori", compute="_compute_workers_count"
    )

    @api.depends("gs_worker_ids")
    def _compute_workers_count(self):
        for record in self:
            record.workers_count = len(record.gs_worker_ids)
