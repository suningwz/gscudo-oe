from odoo import fields, models


class HrDepartment(models.Model):
    _inherit = "hr.department"

    department_code = fields.Char(string="Codice Dipartimento")
