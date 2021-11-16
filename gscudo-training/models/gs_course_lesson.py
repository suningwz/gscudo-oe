from odoo import api, fields, models


class GSLesson(models.Model):
    _name = 'gs_course_lesson'
    _description = 'Lezione'

    name = fields.Char(string='Name')
    gs_course_id = fields.Many2one(comodel_name='gs_course', string='Corso')
    #gs_course_type_id  = fields.Many2many(related="gs_course_id.gs_course_type_id", comodel_name='gs_course_type', string='Tipo Corso')
    
    #gs_course_type_module_id = fields.Many2one(comodel_name='gs_course_type_module', string='Modulo', domain="[('gs_course_type_id','=',gs_course_type_id)]")
    start_time = fields.Datetime(string='Inizio')
    duration =  fields.Float(string='Durata in ore')
    end_time = fields.Datetime(string='Termine')
    location_partner_id = fields.Many2one(comodel_name='Sede', string='Sede')
    teacher_partner_id = fields.Many2one(comodel_name='res.partner', string='Docente')
    coteacher_partner_id    = fields.Many2one(comodel_name='res.partner', string='Co docente')
  


class GSCourse(models.Model):
    _inherit = 'gs_course'

    gs_course_lesson_ids = fields.One2many(comodel_name='gs_course_lesson', inverse_name='gs_course_id', string='Lezioni')
    
