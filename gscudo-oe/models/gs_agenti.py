from odoo import api, fields, models


class GSAgenti(models.Model):
    _name = 'lgit_agenti'
    _description = 'Agenti'
    _inherits='res.partner'

    zonaagente = fields.Char(string='Zona Agente')
    