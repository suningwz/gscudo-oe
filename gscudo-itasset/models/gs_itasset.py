# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ItAsset(models.Model):
    _name = 'gs_itasset'
    _description = 'Assets per la gestione dell''IT e dei dipendenti'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Cespite", track_visibility=True)
    description = fields.Char(string="Descrizione" ,track_visibility=True)
    active = fields.Boolean(string='Attivo' , default= True ,track_visibility=True)
    itasset_type_id = fields.Many2one(comodel_name='gs_itasset_type', string='Tipologia',  track_visibility=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Assegnatario',  track_visibility=True)
    note = fields.Text(string='Annotazioni')
    
    