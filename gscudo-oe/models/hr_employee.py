from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    is_resource = fields.Boolean(string="È una risorsa")
    is_external = fields.Boolean(string="È un esterno")
