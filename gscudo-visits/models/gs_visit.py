from odoo import fields, models


class GSVisit(models.Model):
    _name = "gs_visit"
    _description = "Visita"
    # _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome")
    visit_scheduler_id = fields.Many2one(
        comodel_name="gs_visit_scheduler",
        string="Referenza scheduler",
    )
    date = fields.Date(string="Data")
