from datetime import datetime
from odoo import fields, models, api


class GSLessonEnrollment(models.Model):
    _name = "gs_lesson_enrollment"
    _description = "Registrazione lezione"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome", compute="_compute_name")

    def _compute_name(self):
        for enrollment in self:
            enrollment.name = enrollment.gs_course_lesson_id.name

    gs_course_lesson_id = fields.Many2one(
        comodel_name="gs_course_lesson",
        string="Lezione",
        tracking=True,
        index=True,
    )
    gs_course_id = fields.Many2one(
        comodel_name="gs_course",
        string="Corso",
        related="gs_course_lesson_id.gs_course_id",
        store=True,
        tracking=True,
        index=True,
    )

    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker",
        string="Lavoratore",
        tracking=True,
        index=True,
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Azienda",
        related="gs_worker_id.contract_partner_id",
        index=True,
    )

    state = fields.Selection(
        string="Stato",
        selection=[
            ("I", "Identificato"),
            ("P", "Proposto"),
            ("A", "Accettato"),
            ("C", "Confermato"),
            ("S", "Scaduto"),
            ("F", "Concluso"),
            ("X", "Annullato"),
        ],
        default="I",
        tracking=True,
    )

    enrollment_date = fields.Date(string="Data di iscrizione", default=datetime.now())
    expiration_date = fields.Date(string="Scadenza iscrizione")

    active = fields.Boolean(string="Attivo", default=True, tracking=True)
    is_attendant = fields.Boolean(string="È presente", default=False, tracking=True)
    attended_hours = fields.Float(
        string="Ore frequentate",
        default=0.0,
    )

    @api.onchange("is_attendant")
    def _onchange_is_attendant(self):
        """
        By default, workers attend the whole lesson.
        """
        if self.gs_course_lesson_id.gs_course_type_module_id.generate_certificate:
            return

        if self.is_attendant:
            self.attended_hours = self.gs_course_lesson_id.duration
        else:
            self.attended_hours = 0.0

    implicit = fields.Boolean(string="Iscrizione implicita", default=True)
    gs_course_enrollment_id = fields.Many2one(
        comodel_name="gs_course_enrollment",
        string="Iscrizione al corso",
        tracking=True,
        index=True,
    )

    gs_course_type_module_id = fields.Many2one(
        comodel_name="gs_course_type_module",
        string="Modulo",
        related="gs_course_lesson_id.gs_course_type_module_id",
        tracking=True,
        index=True,
    )

    previous_enrollment_id = fields.Many2one(
        comodel_name="gs_lesson_enrollment",
        string="Lezione precedente",
        tracking=True,
        index=True,
    )

    def get_next_enrollment(self):
        """
        Returns the next enrollment for the worker, or False if this is the last one.
        """
        self.ensure_one()
        enrollment = self.search([("previous_enrollment_id", "=", self.id)])
        return enrollment if len(enrollment) > 0 else False

    def get_possible_reenrollments(self):
        """
        Given a single enrollment, return all possible previous enrollments.
        """
        self.ensure_one()

        non_attended_enrollments = self.search(
            [
                ("gs_worker_id", "=", self.gs_worker_id),
                (
                    "gs_course_id.gs_course_type_id.gs_certificate_type_id",
                    "=",
                    self.gs_course_id.gs_course_type_id.gs_certificate_type_id,
                ),
                ("is_attendant", "=", False),
                ("previous_enrollment.is_attendant", "=", True),
                ("gs_course_lesson_id.generate_certificate", "=", False),
            ]
        )

        possible_enrollments = [
            s.get_next_enrollment() for s in non_attended_enrollments
        ]

        # return sorted(
        #     possible_enrollments,
        #     key=functools.cmp_to_key(
        #         lambda x, y: -1 if y is False or (x is not False and x < y) else 1
        #     ),
        # )

        return possible_enrollments

    def generate_certificate(self):
        """
        Generate certificates for the workers that passed the final test.
        """
        for test in self:
            if not test.is_attendant:
                continue

            certificate_type = (
                # fmt: off
                test
                .gs_course_id
                .gs_course_type_id
                .gs_training_certificate_type_id
                # fmt: on
            )

            if self.env["gs_worker_certificate"].search([("test_id", "=", test.id)]):
                # Certificate already generated
                continue

            enrollments = []
            curr = test

            while curr.id is not False:
                enrollments.append(curr)
                curr = curr.previous_enrollment_id

            attended_hours = sum([e.attended_hours for e in enrollments])

            if (
                attended_hours
                < test.gs_course_id.duration * test.gs_course_id.min_attendance
            ):
                # worker attendance was not high enough
                continue

            if test.is_attendant:
                self.env["gs_worker_certificate"].create(
                    {
                        "gs_worker_id": test.gs_worker_id.id,
                        "gs_training_certificate_type_id": certificate_type.id,
                        "is_update": test.gs_course_id.gs_course_type_id.is_update,
                        "type": "C",
                        "issue_date": test.gs_course_lesson_id.start_time.date(),
                        "test_id": test.id,
                        "attended_hours": attended_hours,
                    }
                )


class GSCourseLesson(models.Model):
    _inherit = "gs_course_lesson"

    gs_worker_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        inverse_name="gs_course_lesson_id",
        string="Iscritti",
    )


class GSCourseEnrollment(models.Model):
    _inherit = "gs_course_enrollment"

    gs_lesson_enrollment_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        inverse_name="gs_course_enrollment_id",
        string="Iscrizione Lezioni",
    )


class GSWorker(models.Model):
    _inherit = "gs_worker"

    gs_lesson_enrollment_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        inverse_name="gs_worker_id",
        string="Lezioni",
        groups="gscudo-training.group_training_backoffice",
    )
