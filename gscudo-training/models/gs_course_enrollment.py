from odoo import api, fields, models, exceptions


class GSEnrollment(models.Model):
    _name = 'gs_course_enrollment'
    _description = 'Registrazione corso'

    name = fields.Char(string='Name')
    gs_course_id = fields.Many2one(comodel_name='gs_course', string='Corso', required=True)
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore', required=True)
    state = fields.Selection(string='Stato', selection=[('I','identificato'),('P', 'proposto'), ('A', 'accettato'),('C','confermato')])
    note=fields.Char(string = 'note', help = 'note', )
    active = fields.Boolean(string='Attivo', default = True)
    
    @api.model
    def create(self, values):
        # At creation add implicit lesson creation
        enrollment = super(GSEnrollment, self).create(values)
        for c in enrollment.gs_course_id.gs_course_lesson_ids:
            data={
                'gs_worker_id':enrollment.gs_worker_id.id,
                'gs_course_lesson_id' : c.id,
                'state':enrollment.state,
                'implicit':True,
                'gs_course_enrollment_id':enrollment.id
            }
            self.env['gs_lesson_enrollment'].create(data)
        return enrollment 

    @api.onchange('state')
    def onchange_state(self):
        for record in self:
            for l in record.gs_lesson_enrollment_ids:
                l.state=record.state
  
  
    def unlink(self):
        for lesson_enrollment in self.gs_lesson_enrollment_ids:
            if lesson_enrollment.is_attendant == True:
                raise exceptions.UserError('Impossibile cancellare iscrizioni con presenze')
            lesson_enrollment.unlink()
        return super(GSEnrollment, self).unlink()


class GSCourse(models.Model):
    _inherit = 'gs_course'

    gs_worker_ids = fields.One2many(comodel_name='gs_course_enrollment', inverse_name='gs_course_id', string='Iscritti')

  
class Worker(models.Model):
    _inherit = 'gs_worker'

    gs_course_enrollment_ids = fields.One2many(comodel_name='gs_course_enrollment', inverse_name='gs_worker_id', string='Corsi')

    
    