from odoo import api, fields, models


class CertificateType(models.Model):
    _name = 'gs_training_certificate_type'
    _description = 'Tipo Certificato Formativo'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Attivo', default = True)
    code = fields.Char(string='Codice')
    renewal_interval = fields.Integer(string='Intervallo rinnovo in anni')
    update_interval = fields.Integer(string='Intervallo aggiornamento in anni')
    
