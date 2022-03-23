from odoo import api, fields, models

import datetime
from datetime import timezone, datetime, timedelta, date
from dateutil.relativedelta import relativedelta

class WorkerMedicalCheck(models.Model):
    _name = 'gs_worker_medical_check'
    _description = 'Esami / Visite'

    name = fields.Char(string='Name', readonly=True)
    active = fields.Boolean(string='Attivo', default = True)
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    
    execution_date = fields.Date(string='Data Esecuzione')
    gs_medical_check_type_id = fields.Many2one(comodel_name='gs_medical_check_type', string='Visita / Esame')
    expiry_date = fields.Date(string='Data Scadenza')
    schedule_time = fields.Datetime(string='Data ora prenotazione')
    gs_medical_check_frequency_id = fields.Many2one(comodel_name='gs_medical_check_frequency', string='Frequenza')
    note = fields.Text(string='Note')

    expired = fields.Boolean(string='Scaduto', compute='_compute_expiration', )
    expiring = fields.Boolean(string='In scadenza', compute='_compute_expiration', )
 
    @api.onchange('gs_medical_check_type_id')
    def _onchange_checktype_id(self):
        for record in self:
            record.gs_medical_check_frequency_id= record.gs_medical_check_type_id.gs_medical_check_frequency_id

    @api.onchange('execution_date','gs_medical_check_frequency_id')
    def _compute_expiry_date(self):
        for record in self:
            if record.execution_date != False and record.gs_medical_check_frequency_id != False:
                record.expiry_date = record.execution_date + relativedelta(
                                years=record.gs_medical_check_frequency_id.year_interval,
                                months=record.gs_medical_check_frequency_id.month_interval,
                                days=record.gs_medical_check_frequency_id.day_interval)

    @api.onchange('gs_worker_id','gs_medical_check_type_id', 'execution_date')
    def _compute_name(self):
        for record in self:
            record.name = "{} {} {} ".format(
                    record.gs_worker_id.name or "", 
                    record.gs_medical_check_type_id.name or "", 
                    record.execution_date.strftime("%Y-%m-%d") if record.execution_date != False else "" )

    @api.depends('expiry_date')
    def _compute_expiration(self):
        for record in self:
            record.expired=False
            record.expiring = False
            if record.expiry_date != False:
                if record.expiry_date < datetime.now().date():
                    record.expired=True
                    record.expiring = False
                elif record.expiry_date < datetime.now().date()+ relativedelta(months=2):
                    record.expired=False
                    record.expiring = True





class GSWorker(models.Model):
    _inherit = 'gs_worker'

    gs_worker_medical_check_ids = fields.One2many(comodel_name='gs_worker_medical_check', inverse_name='gs_worker_id', string='Visite/ Analisi',
         groups="gscudo-surveillance.group_surveillance_backoffice")
    
    
    