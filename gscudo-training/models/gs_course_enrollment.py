from odoo import api, fields, models
from odoo.exceptions import UserError


class GSCourseEnrollment(models.Model):
    _name = "gs_course_enrollment"
    _description = "Registrazione corso"

    # TODO course enrollment name
    name = fields.Char(string="Nome")
    gs_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso", required=True
    )
    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", required=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Azienda",
        related="gs_worker_id.contract_partner_id",
    )
    state = fields.Selection(
        string="Stato",
        selection=[
            # ("I", "Identificato"),
            ("P", "Proposto"),
            ("A", "Accettato"),
            ("C", "Confermato"),
        ],
        default="P",
    )

    note = fields.Char(string="Note")
    active = fields.Boolean(string="Attivo", default=True)

    @api.model
    def create(self, values):
        """
        At creation, add implicit lesson enrollment.
        """
        enrollment = super().create(values)
        lesson_enrollments = []
        for lesson in enrollment.gs_course_id.gs_course_lesson_ids:
            lesson_enrollments.append(
                self.env["gs_lesson_enrollment"].create(
                    {
                        "gs_worker_id": enrollment.gs_worker_id.id,
                        "gs_course_lesson_id": lesson.id,
                        "state": enrollment.state,
                        "implicit": True,
                        "gs_course_enrollment_id": enrollment.id,
                    }
                )
            )

        # for e in lesson_enrollments:
        #     e.previous_enrollment_id = next(
        #         iter(
        #             pe
        #             for pe in lesson_enrollments
        #             if pe.gs_course_lesson_id == e.gs_course_lesson_id.prev_lesson()
        #         ),
        #         False,
        #     )

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
