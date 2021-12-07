from odoo import api, fields, models

import datetime

class WorkerJob(models.Model):
    _name = 'gs_worker_job'
    _description = 'Mansione/Delega'

    name = fields.Char(string='Name', compute="_compute_name", store=True)
    @api.depends('gs_worker_contract_id','gs_worker_id', 'start_date')
    def _compute_name(self):
        for record in self:
            record.name = "{}/{}/{}".format(record.gs_worker_contract_id.id or 0,
                record.gs_worker_id.id or 0 ,
                (record.start_date or datetime.date.today()).strftime("%Y-%m-%d")
            )
    
    active = fields.Boolean(string='Attivo', default=True)
    gs_worker_contract_id = fields.Many2one(comodel_name='gs_worker_contract', string='Contratto')
    gs_worker_id = fields.Many2one(related="gs_worker_contract_id.gs_worker_id", comodel_name='gs_worker', string='Lavoratore')
    
    gs_worker_job_type_id = fields.Many2one(comodel_name='gs_worker_job_type', string='Mansione ')
    
    start_date = fields.Date(string='Data inizio', required=True)
    end_date = fields.Date(string='Data fine')
    job_description = fields.Char(string='Mansione')
    department = fields.Char(string='Reparto/ufficio')
    note  = fields.Char(string='Note')
    sg_job_careers_id  = fields.Integer(string='ID Sawgest')
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



class GSWorker(models.Model):
    _inherit = 'gs_worker'

    gs_worker_job_ids = fields.One2many(comodel_name='gs_worker_job', inverse_name='gs_worker_id', string='Mansioni')
    
    
    