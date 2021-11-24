from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

import datetime
from datetime import timezone, datetime, timedelta

class WorkerContract(models.Model):
    _name = 'gs_worker_contract'
    _description = 'Relazione Worker Partner'

    name = fields.Char(string='Nome')
    active = fields.Boolean(string='Attivo')
    
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Azienda/Sede')
    employee_serial = fields.Char(string='Matricola dip.')
    start_date = fields.Date(string='Data inizio')
    end_date = fields.Date(string='Data fine')
    job_description = fields.Char(string='Mansione')
    department = fields.Char(string='Reparto/ufficio')
    
    
    @api.constrains('start_date', 'end_date')
    def _check_date(self):
        if self.start_date > self.end_date:
            raise ValidationError(
                'La data di fine  deve essere maggiore di quella di inizio')
        if self.start_date < datetime.now() + timedelta(year=-20):
            raise ValidationError(
                'La data di inizio   deve essere negli ultimi 365 giorni')
        if self.end_date != False  and self.end_date > datetime.now() + timedelta(days=365):
            raise ValidationError(
                'La data di fine   deve essere entro i prossimi 365 giorni')
        


   
class ModuleName(models.Model):
    _inherit = 'gs_worker'

    gs_worker_contract_id = fields.Many2one(comodel_name='gs_worker_contract', string='Impiego attuale', 
                                            domain="[('gs_worker_id'),'=',id]")
    contract_partner_id = fields.Many2one(related="gs_worker_contract_id.partner_id", comodel_name='res.partner', string='Azienda/Sede')
    contract_employee_serial = fields.Char(related="gs_worker_contract_id.employee_serial", string='Matricola dip.')
    contract_start_date = fields.Date(related="gs_worker_contract_id.start_date", string='Data inizio')
    contract_end_date = fields.Date(related="gs_worker_contract_id.end_date", string='Data fine')
    contract_job_description = fields.Char(related="gs_worker_contract_id.job_description", string='Mansione')
    contract_department = fields.Char(related="gs_worker_contract_id.department", string='Reparto/ufficio')
    

    gs_worker_contract_ids = fields.One2many(comodel_name='gs_worker_contract', inverse_name='gs_worker_id', string='')
    
    
