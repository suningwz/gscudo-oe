from odoo import api, fields, models


class GSEnrollment(models.Model):
    _name = 'gs_course_enrollment'
    _description = 'Registrazione corso'

    name = fields.Char(string='Name')
    gs_course_id = fields.Many2one(comodel_name='gs_course', string='Corso')
    gs_course_lesson_id = fields.Many2one(comodel_name='gs_course_lesson', string='Lezione')
    gs_employee_id = fields.Many2one(comodel_name='gs_employee', string='Lavoratore')
    state