from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


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

    parent_lesson_id = fields.Many2one(
        comodel_name="gs_course_lesson", string="Lezione padre"
    )
    children_lesson_ids = fields.One2many(
        comodel_name="gs_course_lesson",
        inverse_name="parent_lesson_id",
        string="Lezioni figlie",
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

    def write(self, vals):
        """
        If a lesson is updated, update all children accordingly.
        """
        for parent in self:
            if not parent.children_lesson_ids:
                continue

            for child in parent.children_lesson_ids:
                if (
                    vals.get("start_time")
                    and vals.get("start_time") != child.start_time
                ):
                    child.start_time = vals["start_time"]
                if (
                    vals.get("teacher_partner_id")
                    and vals.get("teacher_partner_id") != child.teacher_partner_id.id
                ):
                    child.teacher_partner_id = vals["teacher_partner_id"]

        return super().write(vals)

    def attend_all(self):
        """
        Set all workers enrolled in the lesson as "have attended".
        """
        self.ensure_one()
        for enrollment in self.gs_worker_ids:
            if enrollment.is_attendant is False:
                enrollment.is_attendant = True
                enrollment.attended_hours = self.duration

    @api.model
    def generate_certificates(self):
        """
        Generate certificates for all workers that passed the final test.
        """
        test = self.browse(self.env.context.get("active_id"))
        # test = self.env.context.get("active_ids")
        # test.ensure_one()

        if not test.gs_course_type_module_id.generate_certificate:
            raise UserError("Questo non è un test finale.")

        for enrollment in test.gs_worker_ids:
            enrollment.generate_certificate()


class GSCourse(models.Model):
    _inherit = "gs_course"

    gs_course_lesson_ids = fields.One2many(
        comodel_name="gs_course_lesson",
        inverse_name="gs_course_id",
        string="Lezioni",
    )

    @api.model
    def create(self, vals):
        """
        Create lessons according to course type modules.
        """
        course = super().create(vals)
        parent = course.parent_course_id

        for module in course.gs_course_type_id.gs_course_type_module_ids:
            data = {
                "name": f"Lezione {module.name}",
                "gs_course_id": course.id,
                "duration": module.duration,
                "gs_course_type_module_id": module.id,
                "location_partner_id": course.location_partner_id.id,
                "state": "tentative",
            }

            if parent is not False and not module.generate_certificate:
                parents = [
                    lesson
                    for lesson in parent.gs_course_lesson_ids
                    if lesson.gs_course_type_module_id == module
                ]

                if parents:
                    lesson = parents[0]
                    data["parent_lesson_id"] = lesson.id
                    data["start_time"] = lesson.start_time
                    data["teacher_partner_id"] = lesson.teacher_partner_id.id

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
