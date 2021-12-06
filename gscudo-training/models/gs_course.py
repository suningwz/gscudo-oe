from odoo import _, api, fields, models


class GSCourse(models.Model):
    _name = 'gs_course'
    _description = 'Corso'

    name = fields.Char(string='Corso')
    protocol= fields.Char(string='Protocollo')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    
    note=fields.Char(string = 'note', help = 'note', )
    active = fields.Boolean(string='Attivo', default = True)
    state = fields.Selection([
            ('1-nuovo', 'Da gestire'),
            ('2-proposto', 'Proposto'),
            ('3-accettato', 'Accettato'),
            ('4-in corso', 'In corso'),
             ('5-concluso', 'Concluso')],string='Stato', default='1-nuovo')
    max_workers=fields.Integer(string = 'Massimo Iscritti', help = 'max_workers', )
    location_partner_id = fields.Many2one(comodel_name='res.partner', string='Sede')
    start_date = fields.Date(string='Data inizio')
    end_date  = fields.Date(string='Data termine')
    gs_course_type_id = fields.Many2one(comodel_name='gs_course_type', string='Tipo Corso')
    elearning  = fields.Boolean(related="gs_course_type_id.elearning", string='Modalità elearning')
    is_multicompany = fields.Boolean(string='Multiazendale')
    
    