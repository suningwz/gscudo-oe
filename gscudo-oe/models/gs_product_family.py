from odoo import _, api, fields, models


class ProductFamily(models.Model):
    _name = 'gs_product_family'
    _description = 'Famiglia'

    name = fields.Char(string='Famiglia')
    code = fields.Char(string='Cod. Famiglia')
    hr_department_id  = fields.Many2one(comodel_name='hr.department', string='Dipartimento')
    manager_id = fields.Many2one(related='hr_department_id.manager_id', comodel_name='hr.employee', string='Supervisore')
    
    
    active = fields.Boolean(string='Attivo', default=True)
    


