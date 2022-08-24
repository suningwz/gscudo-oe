from datetime import timedelta
import datetime
from odoo import fields, models, api
from odoo.exceptions import UserError


class GSWorkerTransferWizard(models.TransientModel):
    _name = "gs_worker_transfer_wizard"
    _description = "Wizard trasferimento dipendenti"

    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Nuova sede", required=True
    )
    old_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Sede attuale", readonly=True
    )

    is_correction = fields.Boolean(string="Correzione", default=False)
    transfer_date = fields.Date(string="Data di trasferimento")
    min_date = fields.Date(string="Data minima", readonly=True)

    @api.onchange("transfer_date")
    def _onchange_transfer_date(self):
        if (
            self.is_correction is False
            and self.transfer_date is not False
            and self.min_date is not False
            and self.transfer_date < self.min_date
        ):
            return {
                "value": {},
                "warning": {
                    "title": "Attenzione!",
                    "message": (
                        "Per alcuni lavoratori la data di assunzione è successiva "
                        "alla data di trasferimento inserita."
                    ),
                },
            }

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id == self.old_partner_id:
            return {
                "value": {},
                "warning": {
                    "title": "Attenzione!",
                    "message": "I lavoratori selezionati lavorano già per questa azienda.",
                },
            }

    def transfer(self):
        """
        Trasfer the selected workers to the selected partners.
        If it is not a correction, close the current contract, open a new one,
        and clone all the current jobs on the new contract.
        """

        if self.is_correction is False and self.transfer_date is False:
            return UserError("Data di trasferimento mancante.")

        workers = self.env["gs_worker"].browse(self.env.context.get("active_ids"))

        for worker in workers:
            if worker.gs_worker_contract_id.partner_id == self.partner_id:
                continue

            if self.is_correction:
                worker.gs_worker_contract_id.partner_id = self.partner_id
            else:
                new_contract = worker.gs_worker_contract_id.copy(
                    default={
                        "start_date": self.transfer_date,
                        "partner_id": self.partner_id.id,
                    }
                )

                worker.gs_worker_contract_id.end_date = self.transfer_date - timedelta(
                    days=1
                )

                for job in worker.gs_worker_contract_id.gs_worker_job_ids:
                    if job.end_date is False or job.end_date > datetime.date.today():
                        job.copy(
                            default={
                                "start_date": self.transfer_date,
                                "gs_worker_contract_id": new_contract.id,
                            }
                        )
                        job.end_date = self.transfer_date - timedelta(days=1)

                worker.gs_worker_contract_id = new_contract


class GSWorker(models.Model):
    _inherit = "gs_worker"

    def transfer_wizard(self):
        """
        Given one or more workers, call the transfer wizard
        """
        if False in [record.gs_worker_contract_id for record in self]:
            raise UserError("Tutti i lavoratori devono avere un contratto attivo.")

        old_partners = set(record.gs_worker_contract_id.partner_id for record in self)
        min_date = max(record.gs_worker_contract_id.start_date for record in self)

        if len(old_partners) != 1:
            raise UserError("Tutti i lavoratori devono lavorare per la stessa azienda.")
        old_partner_id = old_partners.pop().id

        action = {
            "name": "Trasferisci...",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "gs_worker_transfer_wizard",
            "context": {
                "default_old_partner_id": old_partner_id,
                "default_min_date": min_date,
                "active_ids": self.env.context.get("active_ids"),
            },
        }

        return action
