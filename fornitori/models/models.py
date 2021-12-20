# -*- coding: utf-8 -*-

from odoo import models, fields, api


class fornitori(models.Model):
    _name = 'fornitori_fornitori'
    _description = 'fornitori_fornitori'
    _inherits={'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', required=True, ondelete='restrict', auto_join=True, index=True,
        string='Related Partner', help='Partner-related data of the user')
    # overridden inherited fields to bypass access rights, in case you have
    # access to the user but not its corresponding partner
    name = fields.Char(related='partner_id.name', inherited=True, readonly=False)
    email = fields.Char(related='partner_id.email', inherited=True, readonly=False)

    zona = fields.Char(string='zona')
    
