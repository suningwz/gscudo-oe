from odoo import models, fields, api


class GSTrainingPlannerEnrollmentWizard(models.TransientModel):
    _name = "gs_training_planner_enrollment_wizard"
    _description = "Wizard di iscrizione da riga d'offerta"

    gs_worker_ids = fields.Many2many(
        comodel_name="gs_worker",
        string="Lavoratori da iscrivere",
        compute="_compute_gs_worker_ids",
    )

    partner_id = fields.Many2one(comodel_name="res.partner", string="Azienda")

    def _compute_gs_worker_ids(self):
        for record in self:
            if record.partner_id:
                record.gs_worker_ids = self.env["gs_worker"].search(
                    [("contract_partner_id", "=", self.partner_id.id)]
                )
            else:
                record.gs_worker_ids = []

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self._compute_gs_worker_ids()
