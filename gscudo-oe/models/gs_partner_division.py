from odoo import fields, models


class PartnerDivison(models.Model):
    _name = "gs_partner_division"
    _description = "Divisione Cliente"

    name = fields.Char(string="Division")
    esolver_division_id = fields.Char(string="Esolver Division ID")
    esolver_zone_id = fields.Char(string="Esolver Zone ID")

    active = fields.Boolean(string="Active", default=True)
