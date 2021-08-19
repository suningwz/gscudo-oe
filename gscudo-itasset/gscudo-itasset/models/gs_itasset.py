# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ItAsset(models.Model):
    _name = 'gs_itasset'
    _description = 'Assets per la gestione dell''IT e dei dipendenti'

    name = fields.Char(string="Cespite")
    description = fields.Char(string="Descrizione")
    active = fields.Boolean(string='Attivo' , default= True)
    itasset_type_id = fields.Many2one(comodel_name='gs_itasset_type', string='Tipologia')
    
    