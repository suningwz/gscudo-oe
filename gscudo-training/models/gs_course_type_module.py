# -*- coding: utf-8 -*-

from odoo import _, api, fields, models


class GSCourseTypeModule(models.Model):
    _name = 'gs_course_type_module'
    _description = 'GS Modulo'

    name = fields.Char(string='Modulo')
    gs_course_type_id = fields.Many2one(comodel_name='gs_course_type', string='Corso')
 
    
class GSCourseType(models.Model):

    _inherit = 'gs_course_type'
    gs_module_ids = fields.One2many(comodel_name='gs_course_type_module', inverse_name='gs_course_type_id', string='Moduli')
    