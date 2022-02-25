from odoo import _, api, fields, models


class PclMeeting(models.Model):
    _name = 'pcl_meeting'
    _description = 'Meeting Periodico'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Meeting', compute='_compute_name',)
    description = fields.Char(string='Descrizione')
    meeting_date = fields.Date(string='Date', required = 'true',)

    department_id = fields.Many2one(comodel_name='hr.department', string='Area/Ufficio')
    
    periodicity = fields.Selection(string='Tipologia', 
        selection=[
            ('M', 'Mensile'), 
            ('S', 'Settimanale'),
            ('A', 'Annuale'),
            ('', 'Non definita'), ] ,
         default='')
    period_start_date = fields.Date(string='Inizio periodo')
    period_end_date = fields.Date(string='Fine periodo')
    guest_ids = fields.Many2many(string="Partecipanti", comodel_name='res.users', )
    
    state  = fields.Selection(selection=
        [('P','Pianificata'), 
            ('E','Effettuata'),
            ('A','Annullata')],
            string='Stato',default='P')
    active = fields.Boolean(string = 'active', help = 'active',default=True)
    

    @api.depends('meeting_date','name','description')
    def _compute_name(self):
        for record in self:
            record.name= "{}-{}/{}".format((record.meeting_date.strftime("%Y-%m-%d") if record.meeting_date != False else ""),\
                record.department_id.name or "" , record.description or "")

    
