# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Credential(models.Model):
    _name = 'gs_credential'
    _description = 'Credenziali di prima assegnazione'
    _inherit = ['mail.thread',
                'mail.activity.mixin']

    name = fields.Char(string="Username",  tracking=True)
    temp_pwd = fields.Char(string="Password", tracking=True)
    environment = fields.Selection(string='Ambiente',
                                   selection=[('1', 'Computer'),
                                              ('2', 'Email'),
                                              ('3', 'SawGest'),
                                              ('4', 'Esolver'), 
                                              ('5', 'Odoo'),])

    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Assegnatario',  tracking=True)

    