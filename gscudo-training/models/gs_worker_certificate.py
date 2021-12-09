from odoo import _, api, fields, models


class WorkerCertificate(models.Model):
    _name = 'gs_worker_certificate'
    _description = 'Certificazioni'

    name = fields.Char(string='Certificazione')
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    gs_training_certificate_type_id = fields.Many2one(comodel_name='gs_training_certificate_type', string='Tipo certificazione')
    type = fields.Selection(string='Tipo', selection=[('C', 'Certificato'), ('E', 'esigenza formativa'),], default='E')
    active = fields.Boolean(string='Attivo', default = True)
    
    issue_date = fields.Date(string='Data attestato')
    issue_serial = fields.Char(string='Protocollo attestato')
    
    expiry_date = fields.Date(string='Data scadenza')
    note  = fields.Char(string='Note')
    
    
    
    
   