from datetime import date
from odoo import fields, models


class GSTrainingNeedMassWizard(models.TransientModel):
    _name = "gs_training_need_mass_wizard"
    _description = "Wizard di creazione di massa di esigenze formative"

    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Tipo di certificato",
        required=True, index=True,
    )

    def create_training_needs(self):
        """
        Create a training need of the selected type for each
        selected worker.
        """
        for worker in self.env.context.get("active_ids"):
            # TODO check if there already is a training need
            self.env["gs_worker_certificate"].create(
                {
                    "gs_worker_id": worker,
                    "type": "E",
                    "gs_training_certificate_type_id": self.gs_training_certificate_type_id.id,
                    "issue_date": date.today(),
                }
            )
