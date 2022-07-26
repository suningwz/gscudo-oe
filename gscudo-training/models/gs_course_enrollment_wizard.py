from odoo import fields, models
from odoo.exceptions import UserError


class GSCourseCertificateEnrollmentWizard(models.TransientModel):
    _name = "gs_course_certificate_enrollment_wizard"
    _description = "Wizard di iscrizione a corso da esigenze"

    gs_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso", required=True
    )

    gs_training_certificate_type_id = fields.Integer()

    def enroll(self):
        """
        Resolve the selected training requirement(s) by enrolling the worker(s) in a course
        of the right type.
        """
        model = self.env["gs_course_enrollment"]
        active_requirements = self.env["gs_worker_certificate"].browse(
            self.env.context.get("active_ids")
        )

        # if any(
        #     requirement.gs_course_enrollment_ids.id is not False
        #     for requirement in active_requirements
        # ):
        #     raise UserError("Esigenza formativa già risolta")

        if model.search(
            [
                ("gs_course_id", "=", self.gs_course_id.id),
                (
                    "gs_worker_id",
                    "in",
                    [
                        requirement.gs_worker_id.id
                        for requirement in active_requirements
                    ],
                ),
            ]
        ):
            raise UserError("Lavoratore già iscritto al corso")

        # TODO return the created stuff view
        for requirement in active_requirements:
            data = {
                "name": f"Iscrizione a {self.gs_course_id.name} ({self.gs_course_id.start_date})",
                "gs_course_id": self.gs_course_id.id,
                "gs_worker_id": requirement.gs_worker_id.id,
                "gs_worker_certificate_id": requirement.id,
                "state": "C",
            }

            model.create(data)


class GSCourseEnrollmentWizard(models.TransientModel):
    _name = "gs_course_enrollment_wizard"
    _description = "Wizard di iscrizione a corso da singolo corso"

    # gs_worker_certificate_ids = fields.Many2many(
    #     comodel_name="gs_worker_certificate",
    #     relation="gs_lol_lmao",
    #     string="Iscrizioni",
    # )

    gs_worker_certificate_id = fields.Many2one(
        comodel_name="gs_worker_certificate",
        string="Lavoratore",
    )

    gs_training_certificate_type_id = fields.Integer()

    def enroll(self):
        """
        Resolve the selected training requirement(s) by enrolling the worker(s) in a course
        of the right type.
        """
        self.ensure_one()

        model = self.env["gs_course_enrollment"]
        course = self.env["gs_course"].browse(self.env.context.get("active_id"))

        if self.gs_worker_certificate_id.gs_course_enrollment_ids.id is not False:
            raise UserError("Esigenza formativa già risolta")

        if model.search(
            [
                ("gs_course_id", "=", course.id),
                ("gs_worker_id", "=", self.gs_worker_certificate_id.gs_worker_id.id),
            ]
        ):
            raise UserError("Lavoratore già iscritto al corso")

        # TODO return the created stuff view
        data = {
            "name": f"Iscrizione a {course.name} ({course.start_date})",
            "gs_course_id": course.id,
            "gs_worker_id": self.gs_worker_certificate_id.gs_worker_id.id,
            "gs_worker_certificate_id": self.gs_worker_certificate_id.id,
            "state": "C",
        }

        model.create(data)
