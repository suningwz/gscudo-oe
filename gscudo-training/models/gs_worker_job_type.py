from odoo import fields, models


class GSWorkerJobType(models.Model):
    _inherit = "gs_worker_job_type"

    gs_certificate_type_ids = fields.Many2many(
        comodel_name="gs_certificate_type",
        string="Certificati/attestazioni richieste",
        groups="gscudo-training.group_training_backoffice",
    )

    gs_training_certificate_type_ids = fields.Many2many(
        comodel_name="gs_training_certificate_type",
        string="Certificati/attestazioni richieste (old)",
        groups="gscudo-training.group_training_backoffice",
    )
