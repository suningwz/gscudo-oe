from odoo import _, api, fields, models


class GSCourse(models.Model):
    _name = 'gs_course'
    _description = 'Corso'

    name = fields.Char(string='Corso')
    protocol= fields.Char(string='Protocollo')
    
    note=fields.Char(string = 'note', help = 'note', )
    active = fields.Boolean(string='Attivo')
    state = fields.Selection(string='Stato', 
                selection=[('PIAN', 'Pianificato'), 
                    ('ATT', 'Attivo'),
                    ('ANN','Annullato'),
                    ('CON','Concluso')])
    max_workers=fields.Integer(string = 'Massimo Iscritti', help = 'max_workers', )
    location_partner_id = fields.Many2one(comodel_name='Sede', string='Sede')
    start_date = fields.Date(string='Data inizio')
    end_date  = fields.Date(string='Data termine')
    
    