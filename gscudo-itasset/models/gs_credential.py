# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Credential(models.Model):
    _name = 'gs_credential'
    _description = 'Credenziali di prima assegnazione'
    _inherit = ['mail.thread',
                'mail.activity.mixin']

    name = fields.Char(string="Username",  tracking=True)
    temp_pwd = fields.Char(string="Password", tracking=True)
    credential_env = fields.Selection(string='Ambiente',
                                      selection=['Dominio', 'Email', 'SawGest',
                                                 'Esolver',  'Odoo', ])

    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Assegnatario',  tracking=True)
