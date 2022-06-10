from odoo import fields, models
from odoo.exceptions import UserError


class GSLessonMassEnrollmentWizard(models.TransientModel):
    _name = "gs_lesson_mass_enrollment_wizard"
    _description = "Wizard di iscrizione di massa per lezioni"

    gs_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso", required=True
    )
    gs_course_lesson_id = fields.Many2one(
        comodel_name="gs_course_lesson",
        string="Lezione",
        required=True,
        domain=[("gs_course_id", "=", gs_course_id)],
    )

    def enroll_workers(self):
        """
        Enroll the selected workers in the selected lesson.
        Skips workers that are already enrolled in the lesson.
        """
        model = self.env["gs_lesson_enrollment"]
        for worker in self.env.context.get("active_ids"):
            data = {
                "gs_course_lesson_id": self.gs_course_lesson_id.id,
                "gs_worker_id": worker,
                "state": "P",
                "implicit": False,
            }
            # TODO test this
            if model.search(
                [
                    ("gs_course_lesson_id", "=", data["gs_course_lesson_id"]),
                    ("gs_worker_id", "=", data["gs_worker_id"]),
                ]
            ):
                # raise UserError("Worker already enrolled in this course")
                continue

            model.create(data)


class GSLessonSingleEnrollmentWizard(models.TransientModel):
    _name = "gs_lesson_single_enrollment_wizard"
    _description = "Wizard di iscrizione singola per lezioni"

    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", required=True
    )

    # is_reenrollment = fields.Boolean(string="È una reiscrizione", default=False)
    # removed_course_id = fields.Many2one(comodel_name="gs_course", string="Corso")
    # removed_course_lesson_id = fields.Many2one(
    #     comodel_name="gs_course_lesson",
    #     string="Lezione",
    #     domain=[("gs_course_id", "=", removed_course_id)],
    # )

    def enroll_worker(self):
        """
        Enroll the selected worker in the selected lesson.
        Raises an error if the worker is already enrolled in the course.
        """
        self.ensure_one()

        # if self.is_reenrollment and self.removed_course_id is False:
        #     raise ValidationError("Lezione da sostituire mancante")

        model = self.env["gs_lesson_enrollment"]

        lesson_model = self.env["gs_course_lesson"]
        gs_course_lesson_id = self.env.context.get("active_id")
        gs_course_lesson = lesson_model.browse([gs_course_lesson_id])

        if model.search(
            [
                ("gs_worker_id", "=", self.gs_worker_id.id),
                ("gs_course_lesson_id", "=", gs_course_lesson_id),
            ]
        ):
            raise UserError("Lavoratore già iscritto alla lezione.")

        # if self.is_reenrollment:
        #     old_enrollment = model.search(
        #         [
        #             ("gs_worker_id", "=", self.gs_worker_id.id),
        #             ("gs_course_lesson_id", "=", self.removed_course_lesson_id.id),
        #         ]
        #     )
        #     if not old_enrollment:
        #         raise ValidationError(
        #             "Il lavoratore non è iscritto alla lezione da sostituire"
        #         )
        #     # TODO sanity check: enrollments are for the same module
        #     previous_enrollment_id = old_enrollment.previous_enrollment_id.id

        #     # delete the enrollment to replace and all subsequent enrollments
        #     while old_enrollment is not False:
        #         next_old_enrollment = old_enrollment.get_next_enrollment()
        #         old_enrollment.unlink()
        #         old_enrollment = next_old_enrollment
        # else:
        #     previous_enrollment_id = False

        # while gs_course_lesson is not False:
        model.create(
            {
                "gs_course_lesson_id": gs_course_lesson.id,
                "gs_worker_id": self.gs_worker_id.id,
                "state": "P",
                "implicit": False,
                # "previous_enrollment_id": previous_enrollment_id,
            }
        )

        # previous_enrollment_id = e.id
        # gs_course_lesson = gs_course_lesson.next_lesson()
