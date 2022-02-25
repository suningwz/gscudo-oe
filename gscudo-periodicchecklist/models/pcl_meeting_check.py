from odoo import api, fields, models

class PclMeetingCheck(models.Model):
    _name = 'pcl_meeting_check'
    _description = 'Verifica Riunione'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(string='Name')
    pcl_meeting_id =  fields.Many2one(comodel_name='pcl_meeting', string='Riunione')
    department_id = fields.Many2one(related="pcl_meeting_id.department_id",  comodel_name='hr.department', string='Area/Ufficio', store=True)
    meeting_date = fields.Date(related="pcl_meeting_id.meeting_date", string='Date', store=True)
    
    pcl_checktype_id = fields.Many2one(comodel_name='pcl_checktype', string='Tipo Verifica',required = 'true',)
    note = fields.Text(string='Annotazioni')
    
    
    @api.depends('name','pcl_checktype_id','pcl_meeting_id')
    def _onchange(self):
        for record in self:
            if record.name == '' and record.pcl_checktype_id != False and record.pcl_meeting_id != False:
                record.name = record.pcl_checktype_id.name + ' ' + record.meeting_date.strftime('%Y-%m-%d')

class PclMeeting(models.Model):
    _inherit="pcl_meeting"

    pcl_meeting_ckeck_ids  = fields.One2many(comodel_name='pcl_meeting_check', inverse_name='pcl_meeting_id', string='Verifiche')
    