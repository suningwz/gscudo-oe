from odoo import api, fields, models


class GSEnrollment(models.Model):
    _name = 'gs_course_enrollment'
    _description = 'Registrazione corso'

    name = fields.Char(string='Name')
    gs_course_id = fields.Many2one(comodel_name='gs_course', string='Corso')
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    state = fields.Selection(string='Stato', selection=[('I','identificato'),('P', 'proposto'), ('A', 'accettato'),('C','confermato')])


class GSCourse(models.Model):
    _inherit = 'gs_course'

    gs_worker_ids = fields.One2many(comodel_name='gs_course_enrollment', inverse_name='gs_course_id', string='Iscritti')
