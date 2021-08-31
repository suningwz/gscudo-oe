from odoo import _, api, fields, models
from datetime import datetime

class CrmLeads(models.Model):
    _inherit = 'crm.lead'
    
    fiscalcode = fields.Char("Fiscal Code", size=16, help="Italian Fiscal Code")   
    pec = fields.Char(
        "Addressee PEC",
    )
 
    tmk_user_id = fields.Many2one(comodel_name='res.users', string='Telemarketing operator', tracking=True)
    gs_partner_division_id =fields.Many2one(comodel_name='gs_partner_division', string='Division', tracking=True)

    position_inail = fields.Char(string='Posizione Inail')
    position_inps = fields.Char(string='Posizione INPS')
    position_cema = fields.Char(string='Posizione CEMA')
    
    cciaa = fields.Char(string='CCIAA')
    nrea = fields.Char(string='N REA')
    
    revenue = fields.Integer('Fatturato')
    balance_year = fields.Integer(string="Anno bilancio", default='')
    employee_qty = fields.Integer('Adetti')
    ateco_id = fields.Many2one("ateco.category", string="Descrizione ATECO 2007")
   

    def createcall(self,calldate):
        if calldate == False:
            calldate=datetime.now() 
        for record in self:
            record.message_subscribe([record.tmk_user_id.id or self.user_id.id],None)
            activity_data = {
                'activity_type_id' : 2,            
                'res_model' : 'crm.lead',
                'res_model_id': self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
                'res_id' :record.id,
                'user_id' : record.tmk_user_id.id or self.user_id.id or self.env.user.id,
                'date_deadline' : calldate,
                'summary': 'Chiamare',
                'activity_category':'default',
                'previous_activity_type_id': False,
                'recommended_activity_type_id': False,
                'user_id': self.user_id.id
                }
            
            self.env['mail.activity'].create(activity_data)
            
   