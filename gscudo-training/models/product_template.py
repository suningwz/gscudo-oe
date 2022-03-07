from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    gs_course_type_id = fields.Many2one(comodel_name='gs_course_type', string='Tipologia di corso')
    