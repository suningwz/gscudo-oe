from odoo import api, fields, models


class GSWorkerJobType(models.Model):
    _inherit = "gs_worker_job"

    gs_training_certificate_type_ids = fields.Many2many(
        comodel_name="gs_training_certificate_type",
        string="Certificati/Attestazioni richieste",
        groups="gscudo-training.group_training_backoffice",
    )

    gs_training_certificate_type_ids = fields.Many2many(
        comodel_name="gs_training_certificate_type",
        string="Certificati/Attestazioni richieste (old)",
        groups="gscudo-training.group_training_backoffice",
    )

    @api.onchange("gs_worker_job_type_id")
    def _onchange_gs_worker_job_type_id(self):
        for record in self:
            for tc in record.gs_worker_job_type_id.gs_training_certificate_type_ids:
                record.gs_training_certificate_type_ids = [(4, tc.id)]
            for (
                tc
            ) in (
                record.gs_worker_job_type_id.gs_worker_job_type.gs_training_certificate_type_ids
            ):
                record.gs_training_certificate_type_ids = [(4, tc.id)]
