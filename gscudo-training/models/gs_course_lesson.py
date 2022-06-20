from datetime import timedelta
import functools
from odoo import api, fields, models
from odoo.exceptions import UserError


class GSCourseLesson(models.Model):
    _name = "gs_course_lesson"
    _description = "Lezione"
    _inherit = ["mail.thread", "mail.activity.mixin", "documents.mixin"]

    def _get_document_folder(self):
        return self.env["documents.folder"].search([("name", "=", "Formazione")])

    def _get_document_tags(self):
        return self.env["documents.tag"].search([("name", "=", "Foglio firme")])

    # TODO lesson name
    name = fields.Char(string="Nome")
    note = fields.Char(string="Note")
    active = fields.Boolean(string="Attivo", default=True, tracking=True)
    gs_course_id = fields.Many2one(comodel_name="gs_course", string="Corso")
    gs_course_type_id = fields.Many2one(
        related="gs_course_id.gs_course_type_id",
        comodel_name="gs_course_type",
        string="Tipo Corso",
    )

    parent_lesson_id = fields.Many2one(
        comodel_name="gs_course_lesson", string="Lezione padre", tracking=True
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
        tracking=True,
    )

    note = fields.Char(string="Note")
    gs_course_type_module_id = fields.Many2one(
        comodel_name="gs_course_type_module",
        string="Modulo",
        domain="[('gs_course_type_id','=',gs_course_type_id)]",
        tracking=True,
    )
    generate_certificate = fields.Boolean(
        related="gs_course_type_module_id.generate_certificate",
        string="Corso finale",
    )

    start_time = fields.Datetime(string="Inizio", tracking=True)
    duration = fields.Float(string="Durata in ore", tracking=True)
    end_time = fields.Datetime(
        string="Termine", compute="_compute_end_time", store=True
    )

    is_closed = fields.Boolean(string="Lezione chiusa", default=False, tracking=True)

    @api.depends("start_time", "duration")
    def _compute_end_time(self):
        for lesson in self:
            if lesson.start_time and lesson.duration:
                lesson.end_time = lesson.start_time + timedelta(hours=lesson.duration)

    location_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Sede", tracking=True
    )
    elearning = fields.Boolean(string="Modalità elearning", tracking=True)

    teacher_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Docente", tracking=True
    )
    is_teacher_remote = fields.Boolean(string="Docente in videoconf.", tracking=True)

    coteacher_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Co-docente", tracking=True
    )
    is_coteacher_remote = fields.Boolean(
        string="Codocente in videoconf.", tracking=True
    )
    meeting_url = fields.Char(string="Link videoconferenza", tracking=True)

    def write(self, vals):
        """
        If a lesson is updated, update all children accordingly.
        For now triggers on change of start_time and teacher_partner_id.
        """
        for lesson in self:
            for child in lesson.children_lesson_ids:
                if (
                    vals.get("start_time")
                    and not vals.get("start_time") != child.start_time
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

    @api.model
    def sorted(self, vals, reverse=False):
        """
        Takes an array of lessons and returns it ordered.
        """
        return sorted(
            vals,
            key=functools.cmp_to_key(
                lambda x, y: (
                    -1
                    if (
                        y.gs_course_type_module_id.generate_certificate
                        and not x.gs_course_type_module_id.generate_certificate
                    )
                    or x.name.lower() < y.name.lower()
                    else 1
                )
            ),
            reverse=reverse,
        )

    def prev_lesson(self):
        """
        Returns the previous lesson in the course, or False if this is the first one.

        This is done by taking all lessons whose module is required for the given lesson,
        ordering them via module requirement in reverse, and taking the first one.
        """
        self.ensure_one()

        return next(
            # TODO rewrite this
            iter(
                self.sorted(
                    [
                        l
                        for l in self.gs_course_id.gs_course_lesson_ids
                        if not l.gs_course_type_module_id.generate_certificate
                        and self.name.lower() > l.name.lower()
                    ],
                    reverse=True,
                )
            ),
            False,
        )

    def next_lesson(self):
        """
        Returns the next lesson in the course, or False if this is the last one.
        """
        self.ensure_one()
        return next(
            # TODO performances
            iter(
                self.sorted(
                    [
                        l
                        for l in self.gs_course_id.gs_course_lesson_ids
                        if l.gs_course_type_module_id.generate_certificate
                        or self.name.lower() < l.name.lower()
                    ],
                )
            ),
            False,
        )

    def close_lesson(self):
        """
        Sets the lesson as closed.
        """
        self.ensure_one()
        if self.is_closed:
            raise UserError("Questa lezione è già chiusa.")
        self.is_closed = True


class GSCourse(models.Model):
    _inherit = "gs_course"

    gs_course_lesson_ids = fields.One2many(
        comodel_name="gs_course_lesson",
        inverse_name="gs_course_id",
        string="Lezioni",
        tracking=True,
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
