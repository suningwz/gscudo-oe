from odoo import fields, models


class Users(models.Model):
    _inherit = "res.users"

    rewo_password = fields.Char(string="Rewo Password", required=False)
