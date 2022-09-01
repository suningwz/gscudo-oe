from odoo import models, fields


class GSCourseEnrollment(models.Model):
    _inherit = "gs_course_enrollment"

    gs_training_planner_id = fields.Many2one(
        comodel_name="gs_training_planner", string="Linea pianificatore"
    )


class GSTrainingPlanner(models.Model):
    _inherit = "gs_training_planner"

    gs_course_enrollment_ids = fields.One2many(
        comodel_name="gs_course_enrollment",
        inverse_name="gs_training_planner_id",
        string="Iscrizioni collegate",
    )

    gs_course_enrollment_count = fields.Integer(
        string="Numero iscrizioni collegate",
        compute="_compute_gs_course_enrollment_count",
    )

    def _compute_gs_course_enrollment_count(self):
        for record in self:
            record.gs_course_enrollment_count = len(record.gs_course_enrollment_ids)
