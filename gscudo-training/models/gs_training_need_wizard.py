from datetime import date
from odoo import fields, models


class GSTrainingNeedMassWizard(models.TransientModel):
    _name = "gs_training_need_mass_wizard"
    _description = "Wizard di creazione di massa di esigenze formative"

    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Tipo di certificato",
        required=True,
    )

    def create_training_needs(self):
        """
        Create a training need of the selected type for each
        selected worker.
        """
        model = self.env["gs_worker_certificate"]
        active_ids = self.env.context.get("active_ids")

        # FIXME how to manage this?
        if model.search(
            [
                ("gs_worker_id", "in", active_ids),
                (
                    "gs_training_certificate_type_id",
                    "=",
                    self.gs_training_certificate_type_id.id,
                ),
            ]
        ):
            # raise UserError("Esigenza formativa già presente")
            pass

        for worker in active_ids:
            # TODO return the created stuff
            model.create(
                {
                    "gs_worker_id": worker,
                    "type": "E",
                    "gs_training_certificate_type_id": self.gs_training_certificate_type_id.id,
                    "issue_date": date.today(),
                }
            )
