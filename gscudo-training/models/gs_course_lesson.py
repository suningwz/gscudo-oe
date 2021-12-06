from odoo import api, fields, models


class GSLesson(models.Model):
    _name = 'gs_course_lesson'
    _description = 'Lezione'

    name = fields.Char(string='Name')
    gs_course_id = fields.Many2one(comodel_name='gs_course', string='Corso')
    gs_course_type_id  = fields.Many2one(related="gs_course_id.gs_course_type_id", comodel_name='gs_course_type', string='Tipo Corso')
    note=fields.Char(string = 'note', help = 'note', )
    gs_course_type_module_id = fields.Many2one(comodel_name='gs_course_type_module', string='Modulo', domain="[('gs_course_type_id','=',gs_course_type_id)]")
    start_time = fields.Datetime(string='Inizio')
    duration =  fields.Float(string='Durata in ore')
    end_time = fields.Datetime(string='Termine')
    location_partner_id = fields.Many2one(comodel_name='res.partner', string='Sede')
    teacher_partner_id = fields.Many2one(comodel_name='res.partner', string='Docente')
    is_teacher_remote  = fields.Boolean(string='Docente in videoconf.')
    
    coteacher_partner_id    = fields.Many2one(comodel_name='res.partner', string='Co docente')
    is_coteacher_remote  = fields.Boolean(string='Codocente in videoconf.')
    meeting_url = fields.Char(string='Link videoconferenza')
    


class GSCourse(models.Model):
    _inherit = 'gs_course'

    gs_course_lesson_ids = fields.One2many(comodel_name='gs_course_lesson', inverse_name='gs_course_id', string='Lezioni')
    
