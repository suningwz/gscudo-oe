from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.project'

    department_id  = fields.Many2one(comodel_name='hr.department', string='Dipartimento')
    