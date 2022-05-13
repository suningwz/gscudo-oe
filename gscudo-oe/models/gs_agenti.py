from odoo import fields, models


class GSAgenti(models.Model):
    _name = "gs_agenti"
    #_name = "lgit_agenti"
    _description = "Agenti"
    _inherits = "res.partner"

    zonaagente = fields.Char(string="Zona Agente")
