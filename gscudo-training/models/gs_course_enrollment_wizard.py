from odoo import fields, models
from odoo.exceptions import UserError


class GSCourseMassEnrollmentWizard(models.TransientModel):
    _name = "gs_course_mass_enrollment_wizard"
    _description = "Wizard di iscrizione di massa per corsi"

    gs_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso", required=True
    )

    def enroll_workers(self):
        """
        Enroll the selected workers in the selected course.
        Skips workers that are already enrolled in the course.
        """
        model = self.env["gs_course_enrollment"]
        for worker in self.env.context.get("active_ids"):
            data = {
                "gs_course_id": self.gs_course_id.id,
                "gs_worker_id": worker,
                "state": "P",
            }
            if model.search(
                [
                    ("gs_course_id", "=", data["gs_course_id"]),
                    ("gs_worker_id", "=", data["gs_worker_id"]),
                ]
            ):
                # raise UserError("Worker already enrolled in this course")
                continue

            model.create(data)


class GSCourseSingleEnrollmentWizard(models.TransientModel):
    _name = "gs_course_single_enrollment_wizard"
    _description = "Wizard di iscrizione singola per corsi"

    gs_worker_id = fields.Many2one(
        comodel_name="gs_worker", string="Lavoratore", required=True
    )

    def enroll_worker(self):
        """
        Enroll the selected worker in the selected courses.
        Raises an error if the worker is already enrolled in the course.
        """
        model = self.env["gs_course_enrollment"]
        data = {
            "gs_course_id": self.env.context.get("active_id"),
            "gs_worker_id": self.gs_worker_id.id,
            "state": "P",
        }
        if model.search(
            [
                ("gs_course_id", "=", data["gs_course_id"]),
                ("gs_worker_id", "=", data["gs_worker_id"]),
            ]
        ):
            raise UserError("Lavoratore già iscritto al corso.")

        model.create(data)
