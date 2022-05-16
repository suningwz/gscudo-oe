import datetime
from odoo import api, fields, models


class WorkerJob(models.Model):
    _name = "gs_worker_job"
    _description = "Mansione/Delega"

    name = fields.Char(string="Name", compute="_compute_name", store=True)

    @api.depends("gs_worker_contract_id", "gs_worker_id", "start_date")
    def _compute_name(self):
        for record in self:
            # pylint: disable-next=consider-using-f-string
            record.name = "{}/{}/{}".format(
                record.gs_worker_contract_id.id or 0,
                record.gs_worker_id.id or 0,
                (record.start_date or datetime.date.today()).strftime("%Y-%m-%d"),
            )

    active = fields.Boolean(string="Attivo", default=True)
    gs_worker_contract_id = fields.Many2one(
        comodel_name="gs_worker_contract", string="Contratto"
    )
    gs_worker_id = fields.Many2one(
        related="gs_worker_contract_id.gs_worker_id",
        comodel_name="gs_worker",
        string="Lavoratore",
    )

    gs_worker_job_type_id = fields.Many2one(
        comodel_name="gs_worker_job_type", string="Ruolo/Mansione"
    )

    start_date = fields.Date(string="Data inizio", required=True)
    end_date = fields.Date(string="Data fine")
    job_description = fields.Char(string="Mansione")
    department = fields.Char(string="Reparto/ufficio")
    note = fields.Char(string="Note")
    sg_job_careers_id = fields.Integer(string="ID SaWGest")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")

    cartsan_id = fields.Integer(string="ID CartSan")

    use_videoterminals = fields.Boolean(string="Usa videoterminali")
    use_company_vehicles = fields.Boolean(string="Usa vericoli aziendali")
    use_forklift = fields.Boolean(string="Usa muletto")
    night_job = fields.Boolean(string="Lavoro notturno")
    work_at_height = fields.Boolean(string="Lavoro in quota")
    work_small_space = fields.Boolean(string="Ambienti confinati")
    move_loads = fields.Boolean(string="Movimento carichi")

    @api.onchange("gs_worker_job_type_id")
    def _onchange_gs_worker_job_type_id(self):
        for record in self:
            if record.job_description is False:
                record.job_description = record.gs_worker_job_type_id.name


class GSWorker(models.Model):
    _inherit = "gs_worker"

    gs_worker_job_ids = fields.One2many(
        comodel_name="gs_worker_job", inverse_name="gs_worker_id", string="Mansioni"
    )
