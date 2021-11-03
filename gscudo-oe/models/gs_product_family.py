from odoo import _, api, fields, models


class ProductFamily(models.Model):
    _name = 'gs_product_family'
    _description = 'Famiglia'

    name = fields.Char(string='Famiglia')
    code = fields.Char(string='Cod. Famiglia')
    active = fields.Boolean(string='Attivo', default=True)
    


