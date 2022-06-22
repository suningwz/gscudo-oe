from odoo import fields, models


class CrmTag(models.Model):
    _inherit = "crm.tag"

    read_group_ids = fields.Many2many(
        comodel_name="res.groups",
        string="Gruppi lettura",
    )
