from odoo import api, fields, models


class GSLessonEnrollment(models.Model):
    _name = 'gs_lesson_enrollment'
    _description = 'Registrazione corso'

    name = fields.Char(string='Name')
    gs_course_lesson_id = fields.Many2one(comodel_name='gs_course_lesson', string='Corso')

    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    state = fields.Selection(string='Stato', selection=[('I','identificato'),('P', 'proposto'), ('A', 'accettato'),('C','confermato')])
    implicit  = fields.Boolean(string='Iscrizione implicta', defualt= True)
    

class GSCourse(models.Model):
    _inherit = 'gs_course_lesson'

    gs_worker_ids = fields.One2many(comodel_name='gs_lessone_enrollment', inverse_name='gs_course_id', string='Iscritti')