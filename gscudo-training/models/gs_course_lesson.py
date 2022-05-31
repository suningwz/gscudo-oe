from datetime import timedelta
from odoo import api, fields, models


class GSCourseLesson(models.Model):
    _name = "gs_course_lesson"
    _description = "Lezione"

    name = fields.Char(string="Nome")
    note = fields.Char(string="Note")
    active = fields.Boolean(string="Attivo", default=True)
    gs_course_id = fields.Many2one(comodel_name="gs_course", string="Corso")
    gs_course_type_id = fields.Many2one(
        related="gs_course_id.gs_course_type_id",
        comodel_name="gs_course_type",
        string="Tipo Corso",
    )

    state = fields.Selection(
        selection=[("tentative", "Provvisorio"), ("final", "Definitivo")],
        string="Stato",
        default="tentative",
    )

    note = fields.Char(string="Note")
    gs_course_type_module_id = fields.Many2one(
        comodel_name="gs_course_type_module",
        string="Modulo",
        domain="[('gs_course_type_id','=',gs_course_type_id)]",
    )
    start_time = fields.Datetime(string="Inizio")
    duration = fields.Float(string="Durata in ore")
    end_time = fields.Datetime(
        string="Termine", compute="_compute_end_time", store=True
    )

    @api.depends("start_time", "duration")
    def _compute_end_time(self):
        for lesson in self:
            if lesson.start_time and lesson.duration:
                lesson.end_time = lesson.start_time + timedelta(hours=lesson.duration)

    location_partner_id = fields.Many2one(comodel_name="res.partner", string="Sede")
    elearning = fields.Boolean(string="Modalità elearning")

    teacher_partner_id = fields.Many2one(comodel_name="res.partner", string="Docente")
    is_teacher_remote = fields.Boolean(string="Docente in videoconf.")

    coteacher_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Co-docente"
    )
    is_coteacher_remote = fields.Boolean(string="Codocente in videoconf.")
    meeting_url = fields.Char(string="Link videoconferenza")


class GSCourse(models.Model):
    _inherit = "gs_course"

    gs_course_lesson_ids = fields.One2many(
        comodel_name="gs_course_lesson",
        inverse_name="gs_course_id",
        string="Lezioni",
    )

    # @api.onchange("gs_course_type_id")
    # def _onchange_gs_course_type_id(self):
    #     """
    #     Create new lessons according to course type modules.
    #     """
    #     for module in self.gs_course_type_id.gs_course_type_module_ids:
    #         data = {
    #             "name": module.name,
    #             "gs_course_id": self.id,
    #             "duration": module.duration,
    #             "gs_course_type_module_id": module.id,
    #             "state": "tentative",
    #         }
    #         self.env["gs_course_lesson"].create(data)

    @api.model
    def create(self, vals):
        """
        Create new course and lessons according to course type modules.
        """
        course = super().create(vals)
        for module in course.gs_course_type_id.gs_course_type_module_ids:
            data = {
                "name": f"Lezione {module.name}",
                "gs_course_id": course.id,
                "duration": module.duration,
                "gs_course_type_module_id": module.id,
                "location_partner_id": course.location_partner_id.id,
                "state": "tentative",
            }
            self.env["gs_course_lesson"].create(data)
        return course

    def unlink(self):
        """
        Delete course and lessons.
        """
        for course in self:
            for lesson in course.gs_course_lesson_ids:
                lesson.unlink()
        return super().unlink()
