# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ItAsset(models.Model):
    _name = 'gs_itasset'
    _description = 'Assets per la gestione dell''IT e dei dipendenti'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Cespite",  tracking=True)
    description = fields.Char(string="Descrizione" , tracking=True)
    active = fields.Boolean(string='Attivo' , default= True , tracking=True)
    #itasset_position = fields.Char(string="Sede")
    itasset_type_id = fields.Many2one(comodel_name='gs_itasset_type', string='Tipologia',  tracking=True)
    employee_id = fields.Many2one(comodel_name='hr.employee', string='Assegnatario',  tracking=True)
    #department = fields.Char(string='Ufficio', related = 'employee_id.department_id.name')
    note = fields.Text(string='Annotazioni')
    
    