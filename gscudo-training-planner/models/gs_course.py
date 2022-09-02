from odoo import models, fields


class GSCourse(models.Model):
    _inherit = "gs_course"

    gs_training_planner_ids = fields.One2many(
        comodel_name="gs_training_planner",
        inverse_name="gs_course_id",
        string="Righe di pianificatore collegate",
    )
