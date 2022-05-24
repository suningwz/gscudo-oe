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

    confirmed = fields.Boolean(string="Confermata", default=True)
    done = fields.Boolean(string="Eseguita", default=False)

    agent_id = fields.Many2one(
        related="visit_scheduler_id.agent_id",
        comodel_name="hr.employee",
        string="Agente",
    )
    technician_id = fields.Many2one(
        related="visit_scheduler_id.technician_id",
        comodel_name="hr.employee",
        string="Tecnico",
    )
    partner_id = fields.Many2one(
        related="visit_scheduler_id.partner_id",
        comodel_name="res.partner",
        string="Sede",
    )
