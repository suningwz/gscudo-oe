# -*- coding: utf-8 -*-
from odoo import models, fields, api

from odoo import _, api, fields, models


class GSCourseType(models.Model):
    _name = 'gs_course_type'
    _description = 'GS Tipo di corso'

    name = fields.Char(string='', required=True)
    code = fields.Char(string='Codice')
    
    product_id  = fields.Many2one(comodel_name='product.product', string='Prodotto')
    elearning  = fields.Boolean(string='Modalità elearning')
    active = fields.Boolean(string='Attivo', default=True)
    duration = fields.Float(string='Durata in ore', default=2 , required=True)
    update_gs_course_type_it = fields.Many2one(comodel_name='gs_course_type', string='Corso Aggiornamento')
    expiration_years = fields.Integer(string='Scadenza anni', required=True, default= 1)
    
    
