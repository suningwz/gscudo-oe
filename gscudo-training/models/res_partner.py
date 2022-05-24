import logging  # pylint: disable=unused-import
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    gs_worker_attentionable_ids = fields.One2many(
        comodel_name="gs_worker",
        inverse_name="contract_partner_id",
        string="Lavoratori attenzionabili",
        domain=[("is_attentionable", "=", True)],
    )

    attentionable_workers_number = fields.Integer(
        string="N. lavoratori attenzionabili",
        compute="_compute_attentionable_workers_number",
    )

    # TODO performances
    @api.depends(
        "gs_worker_ids.is_attentionable",
        "gs_worker_ids",
    )
    def _compute_attentionable_workers_number(self):
        for partner in self:
            partner.attentionable_workers_number = len(
                [worker for worker in partner.gs_worker_ids if worker.is_attentionable]
            )
