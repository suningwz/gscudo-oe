# -*- coding: utf-8 -*-

from operator import index
from odoo import _, api, fields, models


class GSCourseTypeModule(models.Model):
    _name = 'gs_course_type_module'
    _description = 'GS Modulo'

    name = fields.Char(string='Modulo')
    active = fields.Boolean(string='Attivo', default = True)
    content = fields.Text(string='Contenuto')
    alternate_id  = fields.Integer(string='alternate_id', compute="_compute_alternate_id", store=True, index=True)
    
    
    def _compute_alternate_id(self):
        for record in self:
            record.alternate_id = record.id

    gs_course_type_id = fields.Many2one(comodel_name='gs_course_type', string='Corso')
    sequence = fields.Integer(string='Sequenza', default = 0 )
    duration = fields.Float(string='Durata in ore')
    generate_certificate  = fields.Boolean(string='Genera Attestato' , default=False)
    elearning  = fields.Boolean(string='Modalità elearning')
    module_required_ids = fields.Many2many(
        comodel_name='gs_course_type_module',
        relation="gs_course_type_module_rel", column1="id", column2="alternate_id", 
        string='Moduli Richiesti / Propedeutici')
    
    
    
class GSCourseType(models.Model):

    _inherit = 'gs_course_type'
    gs_course_type_module_ids = fields.One2many(comodel_name='gs_course_type_module', inverse_name='gs_course_type_id', string='Moduli')
    