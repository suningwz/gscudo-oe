from odoo import fields, models


class ResPartnerCategory(models.Model):
    _inherit = "res.partner.category"

    read_group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Gruppi lettura",
    )
