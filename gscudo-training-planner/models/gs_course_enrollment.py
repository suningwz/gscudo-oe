from odoo import models, fields, api


class GSCourseEnrollment(models.Model):
    _inherit = "gs_course_enrollment"

    gs_training_planner_id = fields.Many2one(
        comodel_name="gs_training_planner", string="Linea pianificatore"
    )
    gs_course_id = fields.Many2one(
        comodel_name="gs_course",
        string="Corso",
        required=True,
        tracking=True,
        index=True,
        store=True,
        compute="_compute_gs_course_id",
        inverse="_pass",  # pylint: disable=method-inverse
    )

    def _compute_partner_id(self):
        for record in self:
            if record.gs_training_planner_id:
                record.partner_id = record.gs_training_planner_id.partner_id
            elif record.gs_worker_id:
                record.partner_id = record.gs_worker_id.partner_id

    @api.depends("gs_training_planner_id")
    def _compute_gs_course_id(self):
        for record in self:
            if record.gs_training_planner_id.gs_course_id:
                record.gs_course_id = record.gs_training_planner_id.gs_course_id

    def _pass(self):
        pass

    # def _inverse_gs_course_id(self):
    #     for record in self:
    #         if record.gs_training_planner_id:
    #             record.gs_training_planner_id = False


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

    @api.depends("gs_course_enrollment_ids")
    def _compute_gs_course_enrollment_count(self):
        for record in self:
            record.gs_course_enrollment_count = len(record.gs_course_enrollment_ids)
