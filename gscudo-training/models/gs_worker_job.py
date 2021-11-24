from odoo import api, fields, models


class WorkerJob(models.Model):
    _name = 'gs_worker_job'
    _description = 'Mansione'

    name = fields.Char(string='Name')
    gs_worker_contract_id = fields.Many2one(comodel_name='gs_worker_contract_id', string='Contratto')
    gs_worker_job_type = fields.Many2one(comodel_name='gs_worker_job_type', string='Mansione Standard')
    
    
    