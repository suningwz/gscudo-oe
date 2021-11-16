from odoo import api, fields, models


class GSEnrollment(models.Model):
    _name = 'gs_course_enrollment'
    _description = 'Registrazione corso'

    name = fields.Char(string='Name')
    gs_course_id = fields.Many2one(comodel_name='gs_course', string='Corso')
    gs_course_lesson_id = fields.Many2one(comodel_name='gs_course_lesson', string='Lezione')
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    state = fields.Selection(string='Stato', selection=[('I','identificato'),('P', 'proposto'), ('A', 'accettato'),('C','confermato')])


class GSLesson(models.Model):
    _inherit = 'gs_course_lesson'

    gs_worker_ids = fields.One2many(comodel_name='gs_course_enrollment', inverse_name='gs_course_lesson_id', string='Iscritti')
