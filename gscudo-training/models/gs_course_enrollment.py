from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


class GSCourseEnrollment(models.Model):
    _name = "gs_course_enrollment"
    _description = "Registrazione corso"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome")
    gs_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso", required=True, tracking=True
    )
    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", required=True, tracking=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Azienda",
        related="gs_worker_id.contract_partner_id",
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

    note = fields.Char(string="Note")
    active = fields.Boolean(string="Attivo", default=True, tracking=True)

    @api.model
    def create(self, values):
        """
        At creation, add implicit lesson enrollment.
        """
        if self.search(
            [
                ("gs_worker_id", "=", values.get("gs_worker_id")),
                ("gs_course_id", "=", values.get("gs_course_id")),
            ]
        ):
            raise UserError("Lavoratore già iscritto al corso.")

        enrollment = super().create(values)

        if "expiration_date" not in values:
            enrollment.expiration_date = enrollment.gs_course_id.end_date

        lesson_enrollments = []
        for lesson in enrollment.gs_course_id.gs_course_lesson_ids:
            lesson_enrollments.append(
                self.env["gs_lesson_enrollment"].create(
                    {
                        "name": enrollment.name,
                        "gs_worker_id": enrollment.gs_worker_id.id,
                        "gs_course_lesson_id": lesson.id,
                        "state": enrollment.state,
                        "implicit": True,
                        "gs_course_enrollment_id": enrollment.id,
                        "enrollment_date": enrollment.enrollment_date,
                        "expiration_date": enrollment.expiration_date,
                    }
                )
            )

        for e in lesson_enrollments:
            e.previous_enrollment_id = next(
                iter(
                    pe
                    for pe in lesson_enrollments
                    if pe.gs_course_lesson_id == e.gs_course_lesson_id.prev_lesson()
                ),
                False,
            )

        return enrollment

    @api.onchange("state")
    def _onchange_state(self):
        for l in self.gs_lesson_enrollment_ids:
            l.state = self.state

    def unlink(self):
        """
        When you delete a course enrollment, also delete all linked lessons enrollments.
        Also, check there are no attendants before deleting a lesson.
        """
        for lesson_enrollment in self.gs_lesson_enrollment_ids:
            if lesson_enrollment.is_attendant is True:
                raise UserError("Impossibile cancellare iscrizioni con presenze")
            lesson_enrollment.unlink()
        return super().unlink()


class GSCourse(models.Model):
    _inherit = "gs_course"

    gs_worker_ids = fields.One2many(
        comodel_name="gs_course_enrollment",
        inverse_name="gs_course_id",
        string="Iscritti",
    )


class Worker(models.Model):
    _inherit = "gs_worker"

    gs_course_enrollment_ids = fields.One2many(
        comodel_name="gs_course_enrollment",
        inverse_name="gs_worker_id",
        string="Corsi",
        groups="gscudo-training.group_training_backoffice",
    )
