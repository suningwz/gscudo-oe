from odoo import fields, models


class WorkerJobType(models.Model):
    _name = "gs_worker_job_type"
    _description = "Tipi Mansione/Delega"

    name = fields.Char(string="Name")
    active = fields.Boolean(string="Attivo", default=True)
    note = fields.Char(string="Note")
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Cliente/sede di riferimento"
    )
    gs_worker_job_type = fields.Many2one(
        comodel_name="gs_worker_job_type",
        string="Mansione Standard",
        domain="[('gs_worker_job_type','=',False)]",
    )

    cartsan_id = fields.Integer(string="ID CartSan")

    use_videoterminals = fields.Boolean(string="Usa videoterminali")
    use_company_vehicles = fields.Boolean(string="Usa vericoli aziendali")
    use_forklift = fields.Boolean(string="Usa muletto")
    night_job = fields.Boolean(string="Lavoro notturno")
    work_at_height = fields.Boolean(string="Lavoro in quota")
    work_small_space = fields.Boolean(string="Ambienti confinati")
    move_loads = fields.Boolean(string="Movimento carichi")
