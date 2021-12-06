from odoo import _, api, fields, models


class Employee(models.Model):
    _inherit = 'hr.employee'

    is_resource = fields.Boolean(string='E\' una risorsa')
    is_external  = fields.Boolean(string='E\' un esterno')
    
    
