from odoo import _, api, fields, models
from datetime import datetime

class CrmLeads(models.Model):
    _inherit = 'crm.lead'

    _sql_constraints = [('vat', 'unique(vat)',
'P.IVA già presente')]

    sg_clients_id  = fields.Integer(string="ID Cliente SaWGest")
    sg_branches_id = fields.Integer(string="ID Ufficio SaWGest ")
    sg_updated_at  = fields.Datetime(string='Data Aggiornamento Sawgest')
    sg_synched_at = fields.Datetime(string='Data ultima Syncronizzazione sawgest')
    

    sg_url = fields.Char(string='Vedi in sawgest' ,compute="_compute_sg_url", store=False )

    
    def _compute_sg_url(self):
        irconfigparam = self.env['ir.config_parameter']
        base_url = irconfigparam.sudo().get_param('sawgest_branches_url')
        if base_url:
            for record in self:
                if record.sg_branches_id and record.sg_branches_id > 0:
                    record.sg_url = base_url.format(record.sg_branches_id)    
                else:
                    record.sg_url = False

    
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
    rating = fields.Integer(string='Rating')
    share_capital = fields.Float(string='Capitale Sociale')
    credit_limit = fields.Float(string='Fido')
    prejudicials = fields.Boolean(string='Pregiudizievoli')
    
    ##### Competitors
    def get_competitor_type(self):
        return [('','non definito '),
                ('int','interno '),
                ('est','esterno ')
                ]
        

    safety_competitor_type  = fields.Selection(get_competitor_type, string='Sicurezza gestione',  default='')
    safety_partner_id = fields.Many2one(string='Conc. Sicurezza', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")

    training_competitor_type  = fields.Selection(get_competitor_type, string='Formazione gestione', default='')
    training_partner_id = fields.Many2one(string='Conc. Formazione', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")
    
    food_competitor_type  = fields.Selection(get_competitor_type, string='Alimentare gestione', default='')
    food_partner_id = fields.Many2one(string='Conc. Alimentare', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")

    machdir_competitor_type  = fields.Selection(get_competitor_type, string='Dirett. Macchine gestione', default='')
    machdir_partner_id = fields.Many2one(string='Conc. Dirett. Macchine', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")

    healthsurv_competitor_type  = fields.Selection(get_competitor_type, string='Sorv. Sanit. gestione', default='')
    healthsurv_partner_id = fields.Many2one(string='Conc. Sorv. Sanit.', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")
    
    environment_competitor_type  = fields.Selection(get_competitor_type, string='Ambientale gestione', default='')
    environment_partner_id = fields.Many2one(string='Conc. Ambientale', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")

    management_competitor_type  = fields.Selection(get_competitor_type, string='Sistemi Gest. gestione', default='')
    management_partner_id = fields.Many2one(string='Conc. Sistemi Gest.', comodel_name='res.partner',
                                        domain="[('is_competitor','=',True)]")

    has_competitors  = fields.Boolean(string='Ci sono concorrenti', compute='_compute_has_competitor', store=True)

    @api.depends('safety_competitor_type', 'training_competitor_type', 'food_competitor_type', 'machdir_competitor_type', 'healthsurv_competitor_type', 'environment_competitor_type')                                  
    def _compute_has_competitor(self):
        for record in self:
            record.has_competitors = False
                
            if  (record.safety_competitor_type == "est" or 
                        record.training_competitor_type == "est" or 
                        record.food_competitor_type == "est" or 
                        record.machdir_competitor_type == "est" or 
                        record.healthsurv_competitor_type == "est" or 
                        record.environment_competitor_type == "est") :
                record.has_competitors = True
                


    
    
    @api.depends('user_id')
    def _onchange_user_id(self):
        for record in self:
            if record.user_id != False:
                if record.user_id.tmk_user_id != False :
                    record.tmk_user_id = record.user_id.tmk_user_id.id



    # def createcall(self,calldate):
    #     if calldate == False:
    #         calldate=datetime.now() 
    #     for record in self:
    #         record.message_subscribe([record.tmk_user_id.id or self.user_id.id],None)
    #         activity_data = {
    #             'activity_type_id' : 2,            
    #             'res_model' : 'crm.lead',
    #             'res_model_id': self.env['ir.model'].search([('model', '=', 'crm.lead')]).id,
    #             'res_id' :record.id,
    #             'user_id' : record.tmk_user_id.id or self.user_id.id or self.env.user.id,
    #             'date_deadline' : calldate,
    #             'summary': 'Chiamare',
    #             'activity_category':'default',
    #             'previous_activity_type_id': False,
    #             'recommended_activity_type_id': False,
    #             'user_id': self.user_id.id
    #             }
            
    #         self.env['mail.activity'].create(activity_data)
            
   