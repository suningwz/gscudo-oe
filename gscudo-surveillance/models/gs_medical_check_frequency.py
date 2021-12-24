from odoo import _, api, fields, models


class MedicalCheckFrequency(models.Model):
    _name = 'gs_medical_check_frequency'
    _description = 'Feraquenza'

    name = fields.Char(string='Frequenza')
    active = fields.Boolean(string='Attivo', default = True)
    
    no_repeat = fields.Boolean(string='Una tantum', default=False , required=True)
    day_interval = fields.Integer(string='Intervallo giorni' , default=0 , required=True)
    month_interval = fields.Integer(string='Intervallo mesi', default=0 , required=True)
    year_interval = fields.Integer(string='Intervallo anni', default=0 , required=True)
    
