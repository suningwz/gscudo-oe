from odoo import models


class GSWorkerCertificate(models.Model):
    _inherit = "gs_worker_certificate"

    def _get_partner_id(self):
        """
        Returns the partner linked to the certificate.
        Raises ValueError if called on a recordset holding multiple certificates.
        """
        self.ensure_one()
        return (
            self.test_id.gs_course_enrollment_id.gs_training_planner_id.partner_id
            or super()._get_partner_id()
        )
