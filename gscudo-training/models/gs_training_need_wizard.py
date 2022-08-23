from datetime import date
from odoo import fields, models, api


class GSTrainingNeedMassWizard(models.TransientModel):
    _name = "gs_training_need_mass_wizard"
    _description = "Wizard di creazione di massa di esigenze formative"

    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Tipo di certificato",
        required=True, index=True,
    )

    @api.onchange("gs_training_certificate_type_id")
    def _onchange_check_existence(self):
        certs = self.env["gs_worker_certificate"].search(
            [
                ("gs_worker_id", "in", self.env.context.get("active_ids")),
                (
                    "gs_training_certificate_type_id",
                    "=",
                    self.gs_training_certificate_type_id.id,
                ),
            ]
        )

        if certs:
            return {
                "value": {},
                "warning": {
                    "title": "Attenzione!",
                    "message": (
                        f"Un lavoratore ha già questa esigenza: {certs.gs_worker_id.name}"
                        if len(certs) == 1
                        else (
                            f"{len(certs)} lavoratori hanno già questa esigenza: "
                            + ", ".join(map(lambda c: c.gs_worker_id.name, certs))
                        )
                    )
                    + ".\nQuesti lavoratori verranno ignorati per la creazione di questa esigenza.",
                },
            }

    def create_training_needs(self):
        """
        Create a training need of the selected type for each
        selected worker.
        """
        model = self.env["gs_worker_certificate"]
        active_ids = self.env.context.get("active_ids")

        # count = 0

        for worker in active_ids:
            if model.search(
                [
                    ("gs_worker_id", "=", worker),
                    (
                        "gs_training_certificate_type_id",
                        "=",
                        self.gs_training_certificate_type_id.id,
                    ),
                ]
            ):
                continue

            model.create(
                {
                    "gs_worker_id": worker,
                    "type": "E",
                    "gs_training_certificate_type_id": self.gs_training_certificate_type_id.id,
                    "issue_date": date.today(),
                }
            )
            # count += 1

        # return {
        #     "value": {},
        #     "warning": {
        #         "title": "Fatto!",
        #         "message": f"{count} esigenze create."
        #         if count != 1
        #         else "Esigenza creata.",
        #     },
        # }
