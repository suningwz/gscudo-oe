# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ResPartner (models.Model):
    _inherit = "res.partner"
    
    sg_clients_id  = fields.Integer(string="ID Cliente SaWGest")
    sg_branches_id = fields.Integer(string="ID Ufficio SaWGest ")
    sg_employee_id = fields.Integer(string="ID Impiegato SaWGest")
    sg_esolver_id = fields.Integer(string="ID ESolver")
    

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

    tmk_user_id = fields.Many2one(comodel_name='res.users', string='Telemarketing operator')
    gs_partner_division_id =fields.Many2one(comodel_name='gs_partner_division', string='Division')


    revenue = fields.Integer('Fatturato')
    balance_year = fields.Integer(string="Anno bilancio", default='')
    employee_qty = fields.Integer('Adetti')
    main_ateco_id = fields.Many2one("ateco.category", string="Descrizione ATECO 2007")
    rating = fields.Integer(string='Rating')
    share_capital = fields.Float(string='Capitale Sociale')
    #credit_limit = fields.Float(string='Fido')
    prejudicials = fields.Boolean(string='Pregiudizievoli')
    
    #### From SAWGest
    
    position_inail = fields.Char(string='Posizione Inail')
    position_inps = fields.Char(string='Posizione INPS')
    position_cema = fields.Char(string='Posizione CEMA')
    cciaa = fields.Char(string='CCIAA')
    nrea = fields.Char(string='N REA')
    cdc_notes=fields.Text(string = 'Note cdc', help = 'cdc_notes', )
    required_cig=fields.Boolean(string = 'Richiesto CIG', help = 'required_cig', )
    cig=fields.Char(string = 'CIG', help = 'cig', )
   
    technical_contact=fields.Char(string = 'Ref. Tecnico', help = 'Ref. Tecnico', )
    technical_contact_notes=fields.Text(string = 'Ref. Tecnico Note', help = 'Note', )
    technical_contact_email=fields.Char(string = 'technical_contact_email', help = 'technical_contact_email', )
    technical_contact_phone=fields.Char(string = 'technical_contact_phone', help = 'technical_contact_phone', )

    administrative_contact=fields.Char(string = 'Contatto Amministrativo', help = 'Contatto Amministrativo', )
    administrative_contact_notes=fields.Text(string = 'Contatto Amministrativo Note', help = 'Note', )
    administrative_contact_email=fields.Char(string = 'administrative_contact_email', help = 'administrative_contact_email', )
    administrative_contact_phone=fields.Char(string = 'administrative_contact_phone', help = 'administrative_contact_phone', )

    employee_number=fields.Integer(string = 'N. Impiegati', help = 'numero impiegati', )

    rspp=fields.Char(string = 'RSPP', help = 'Nominativo RSPP', )
    rspp_notes=fields.Text(string = 'RSPP Note', help = 'Note RSPP', )
    rls=fields.Char(string = 'RLS', help = 'Nominativo RLS', )
    fire_officer=fields.Char(string = 'Resp. Antincedio', help = 'fire_officer', )
    prevention_managers_number=fields.Integer(string = 'Numero Addetti ', help = 'prevention_managers_number', )
    managers_number=fields.Integer(string = 'Nr Dirigenti', help = 'managers_number', )
    fire_officers_number=fields.Integer(string = 'Nr Addetti Antincendio', help = 'fire_officers_number', )
    first_aid_attendants_number=fields.Integer(string = 'Nr Addetti Primo Soccorso', help = 'first_aid_attendants_number', )
    evacuation_coordinators_number=fields.Integer(string = 'Nr Addetti Evaquazione', help = 'evacuation_coordinators_number', )
    doctor=fields.Char(string = 'Medico', help = 'doctor', )
    doctor_notes=fields.Text(string = 'Medico Note', help = 'doctor_notes', )
    spring_code=fields.Char(string = 'spring_code', help = 'spring_code', )

    is_saleagent = fields.Boolean(string='Agente', default=False)
    is_telemarketer = fields.Boolean(string='Telemarketer', default=False)
    is_competitor = fields.Boolean(string="E' un competitor", default=False)

    #competitors
    def get_competitor_type(self):
        return [
                ('','n/d'),
                ('interna','interna'),
                ('esterna','esterna')
                ]
        

    # safety_competitor_type  = fields.Selection(get_competitor_type,string='Sicurezza gestione', 
    #                                             default='')
    # safety_partner_id = fields.Many2one(string='Sicurezza Competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")

    # training_competitor_type  = fields.Selection(get_competitor_type,string='Sicurezza gestione', 
    #                                             default='')
    # training_partner_id = fields.Many2one(string='Formazione competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")
    
    # food_competitor_type  = fields.Selection(get_competitor_type,string='Sicurezza gestione', 
    #                                             default='')
    # food_partner_id = fields.Many2one(string='Alimentare competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")

    # machdir_competitor_type  = fields.Selection(get_competitor_type,string='Sicurezza gestione', 
    #                                             default='')
    # machdir_partner_id = fields.Many2one(string='Dirett. Macchine competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")

    # healthsurv_competitor_type  = fields.Selection(string='Sorv. Sanit. gestione', 
    #                                            selection= get_competitor_type(), default='')
    # healthsurv_partner_id = fields.Many2one(string='Sorv. Sanit. competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")
    # environment_competitor_type  = fields.Selection(string='Ambientale gestione', 
    #                                            selection= get_competitor_type(), default='')
    
    # environment_partner_id = fields.Many2one(string='Ambientale competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")
    # management_competitor_type  = fields.Selection(string='Sistemi Gest. gestione', 
    #                                            selection= get_competitor_type(), default='')
    # management_partner_id = fields.Many2one(string='Sistemi Gest. competitor', comodel_name='res.partner',
    #                                     domain="[('is competitor','=',True)]")



    
    
    @api.onchange('user_id')
    def _onchange_user_id(self):
        for record in self:
            if record.user_id.tmk_user_id != False :
                record.tmk_user_id = record.user_id.tmk_user_id.id
 
