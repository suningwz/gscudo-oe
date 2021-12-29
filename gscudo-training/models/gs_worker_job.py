from odoo import _, api, fields, models


class WorkerJobType(models.Model):
    _inherit = 'gs_worker_job'

    gs_training_certificate_type_ids = fields.Many2many(comodel_name='gs_training_certificate_type', string='Certificati/attestazioni richieste')
    
     
    @api.onchange('gs_worker_job_type_id')
    def _onchange_gs_worker_job_type_id(self):
        for record in self:
            for tc in record.gs_worker_job_type_id.gs_training_certificate_type_ids:
                record.gs_training_certificate_type_ids=[(4,tc.id)]    
            for tc in record.gs_worker_job_type_id.gs_worker_job_type.gs_training_certificate_type_ids:
                record.gs_training_certificate_type_ids=[(4,tc.id)]    

            