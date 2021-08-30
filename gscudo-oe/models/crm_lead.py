from odoo import _, api, fields, models
from datetime import datetime

class CrmLeads(models.Model):
    _inherit = 'crm.lead'

    tmk_user_id = fields.Many2one(comodel_name='res.users', string='Telemarketing operator', tracking=True)
    gs_partner_division_id =fields.Many2one(comodel_name='gs_partner_division', string='Division', tracking=True)

    position_inail = fields.Char(string='Posizione Inail')
    position_inps = fields.Char(string='Posizione INPS')
    position_cema = fields.Char(string='Posizione CEMA')
    


    def createcall(self):
        for record in self:
            record.message_subscribe([record.tmk_user_id.id or self.user_id.id],None)
            activity_data = {
                'activity_type_id' : 2,            
                'res_model' : 'crm.lead',
                'res_model_id': self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                'res_id' :record.id,
                'user_id' : record.tmk_user_id.id or self.user_id.id,
                'date_deadline' : datetime.now() ,
                'summary': 'Chiamare',
                'activity_category':'default',
                'previous_activity_type_id': False,
                'recommended_activity_type_id': False,
                'user_id': self.user_id.id
                }
            
            self.env['mail.activity'].create(activity_data)