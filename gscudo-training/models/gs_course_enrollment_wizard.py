from datetime import datetime

from odoo import fields, models
from odoo.exceptions import UserError


class GSCourseSingleCertificateEnrollmentWizard(models.TransientModel):
    _name = "gs_course_single_certificate_enrollment_wizard"
    _description = "Wizard di iscrizione a corso da singola esigenza"

    gs_course_id = fields.Many2one(
        comodel_name="gs_course",
        string="Corso",
        required=True,
        # FIXME domain on view
        # domain=[
        #     (
        #         "gs_course_type_id.gs_training_certificate_type_id.id",
        #         "=",
        #         record.gs_training_certificate_type_id.id,
        #     ),
        #     ("start_date", ">", datetime.now().date()),
        # ],
    )

    # FIXME finish
    def enroll(self):
        """
        Resolve the training requirement by enrolling the worker in a course
        of the right type.
        """
        model = self.env["gs_course_enrollment"]
        active_enrollments = (
            self.env["gs_course_enrollment"].browse(
                [self.env.context.get("active_id")]
            )
        )
        if len(active_enrollments) != 1:
            raise UserError("Errore nell'iscrizione")
            
        data = {
            "name": f"Iscrizione per {self.gs_worker_id.name}",
            "gs_course_id": self.gs_course_id.id,
            # self.env.context.get("active_id"),
            "gs_worker_id": self.env["gs_course_enrollment"].browse(
                [self.env.context.get("active_id")]
            ),
            "state": "C",
        }
