from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError


class GSPlannerCertificateEnrollmentWizard(models.TransientModel):
    _name = "gs_planner_certificate_enrollment_wizard"
    _description = "Wizard di iscrizione a corso da esigenze via planner"

    gs_planner_id = fields.Many2one(
        comodel_name="gs_planner", string="Riga pianificatore", required=True
    )

    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_course_type",
        compute="_compute_gs_training_certificate_type_id",
    )

    def _compute_gs_training_certificate_type_id(self):
        for record in self:
            active_requirements = self.env["gs_worker_certificate"].browse(
                self.env.context.get("active_ids")
            )

            ids = set(
                requirement.gs_worker_id.contract_partner_id
                for requirement in active_requirements
            )
            if len(ids) != 1:
                raise ValidationError("Selezionate esigenze di tipo diverso.")

            record.gs_training_certificate_type_id = ids.pop()

    @api.onchange("gs_planner_id")
    def _onchange_gs_planner_id(self):
        active_requirements = self.env["gs_worker_certificate"].browse(
            self.env.context.get("active_ids")
        )

        if (
            len(
                set(
                    requirement.gs_worker_id.contract_partner_id
                    for requirement in active_requirements
                )
            )
            > 1
        ):
            return {
                "value": {},
                "warning": {
                    "title": "Attenzione!",
                    "message": "I lavoratori selezionati lavorano per aziende diverse.",
                },
            }

        if not self.gs_planner_id:
            return

        certs = self.env["gs_course_enrollment"].search(
            [
                ("gs_course_id", "=", self.gs_planner_id.gs_course_id.id),
                (
                    "gs_worker_id",
                    "in",
                    [
                        requirement.gs_worker_id.id
                        for requirement in active_requirements
                    ],
                ),
            ]
        )

        if certs:
            message = (
                "Lavoratore già iscritto a questo corso.\n"
                if len(certs) == 1
                else f"{len(certs)} lavoratori sono già iscritti a questo corso.\n"
            )

            return {
                "value": {},
                "warning": {
                    "title": "Attenzione!",
                    "message": message,
                },
            }

    def enroll(self):
        """
        Resolve the selected training requirement(s) by enrolling the worker(s) in a course
        of the right type, selected via the connected planner line.
        """
        model = self.env["gs_course_enrollment"]
        active_requirements = self.env["gs_worker_certificate"].browse(
            self.env.context.get("active_ids")
        )

        if (
            len(
                set(
                    requirement.gs_worker_id.contract_partner_id
                    for requirement in active_requirements
                )
            )
            > 1
        ):
            raise UserError("I lavoratori selezionati lavorano per aziende diverse.")

        if (
            len(
                set(
                    requirement.gs_worker_id.contract_partner_id
                    for requirement in active_requirements
                )
            )
            > 1
        ):
            raise ValidationError("Selezionate esigenze di tipo diverso.")

        for requirement in active_requirements:
            if model.search(
                [
                    ("gs_course_id", "=", self.planner_id.gs_course_id.id),
                    ("gs_worker_id", "=", requirement.gs_worker_id.id),
                ]
            ):
                continue

            data = {
                "name": f"Iscrizione a {self.gs_course_id.name} ({self.gs_course_id.start_date})",
                "gs_training_planner_id": self.planner_id.id,
                "gs_worker_id": requirement.gs_worker_id.id,
                "gs_worker_certificate_id": requirement.id,
                "state": "C",
            }

            model.create(data)
