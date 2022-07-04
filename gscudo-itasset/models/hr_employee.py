from odoo import fields, models


class Employee(models.Model):
    _inherit = "hr.employee"

    itasset_ids = fields.One2many(
        comodel_name="gs_itasset", inverse_name="employee_id", string="Attrezzature IT"
    )
    credential_ids = fields.One2many(
        comodel_name="gs_credential",
        inverse_name="employee_id",
        string="Credenziali di Default",
    )
