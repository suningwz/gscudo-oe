from odoo import api, fields, models


class WorkerJob(models.Model):
    _name = 'gs_worker_job_type'
    _description = 'Tipi Mansione/Delega'


    name = fields.Char(string='Name')
    active = fields.Boolean(string='Attivo', default=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente/sede di riferimento')
    gs_worker_job_type = fields.Many2one(comodel_name='gs_worker_job_type', string='Mansione Standard')

    cartsan_id  = fields.Integer(string='ID CartSan')

    use_videoterminals = fields.Boolean(
        string='use_videoterminals', help='Usa videoterminali', )
    use_company_vehicles = fields.Boolean(
        string='Usa vericoli aziendali', help='use_company_vehicles', )
    use_forklift  = fields.Boolean(string='Usa muletto')
    night_job = fields.Boolean(string='Lavoro notturno', help='night_job', )
    work_at_height = fields.Boolean(
        string='Lavoro in quota', help='work_at_height', )
    work_small_space = fields.Boolean(string='Ambienti confinati')
    move_loads = fields.Boolean(string='Movimento carichi')
    
    
    
    