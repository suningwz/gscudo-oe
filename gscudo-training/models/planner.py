from odoo import _, api, fields, models


class Planner(models.Model):
    _name = 'gstraining_planner'
    _description = 'Pianificatore'
    _inherit = ['mail.thread', 
                'mail.activity.mixin']


    # field connected to Sawgest data
    gs_client_id= fields.Many2one(comodel_name='gs_clients', string='Cliente',  tracking=True,)
    gs_offer_id  = fields.Many2one(comodel_name='gs_offers', string='Offerta', domain="[('client_id','=', gs_client_id)]" ,tracking=True,)
    gs_offer_items_id  = fields.Many2one(comodel_name='gs_offer_items', string='Riga Offerta', domain="[('offer_id','=', gs_offer_id)]" ,tracking=True,)
    gs_article_id = fields.Many2one(comodel_name='gs_articles', string='Articolo', tracking=True,)
    gs_training_class_course_id = fields.Many2one(comodel_name='gs_training_class_courses', string='Corso', tracking=True,)

    gs_training_class_id = fields.Many2one(related="gs_training_class_course_id.training_class_id", comodel_name='gs_training_classes', string='Classe')
    gs_offer_issue_date = fields.Date(related="gs_offer_id.issue_date",string='Data Offerta')
    
    
    # fields for administrations teams
    invoice_ref = fields.Char(string='Fatture', tracking=True, )
    
    # fields for training staff teams
    place = fields.Char(string='Luogo', tracking=True, )

    #tutor  = fields.Char(string='Fornitore', tracking=True, )
    tutor_price = fields.Float(string='Docenza prezzo', tracking=True, )
    tutor_order_ref = fields.Char(string='Rif. ordine docente', tracking=True, )
    


    
    name = fields.Char(string='Corso', tracking=True, )
    course_date = fields.Date(string='Data', tracking=True, )
    lesson_dates= fields.Char(string='Date corso', tracking=True, )
    lesson_times = fields.Char(string='Orario', tracking=True, )
    
    place_supplier = fields.Char(string='Fornitore Sala', tracking=True, )
    place_price = fields.Float(string='Prezzo Sala', tracking=True, )
    place_order_ref = fields.Char(string='Rif. ordine sala', tracking=True, )
    material_supplier = fields.Char(string='Fornitore Materali', tracking=True, )
    material_price = fields.Float(string='Prezzo Materiali', tracking=True, )
    material_order_ref = fields.Char(string='Rif. ordine materiali', tracking=True, )
    
    note = fields.Text(string='Note',   )
    
    course_attendants = fields.Integer(string='Partecipanti', tracking=True, )
    tot_qty = fields.Integer(string='Q.tà', tracking=True, )
    tot_hours = fields.Float(string='Nr. Ore', tracking=True, )
    course_price = fields.Float(string='Prezzo unitario')
    
    
    @api.onchange('gs_client_id')
    def onchange_client_id(self):
        for rec in self:
            if rec.gs_client_id.id != False:
                if rec.gs_offer_id.client_id.id != rec.gs_client_id.id:
                    rec.gs_offer_id = False
                return {'domain': {'gs_offer_id': [('offer_state_id','in', [2,10]),('deleted_at','=',False),('client_id', '=', rec.gs_client_id.id)]}}

    @api.onchange('gs_offer_id')
    def onchange_gs_offer_id(self):
        for rec in self:
            if rec.gs_offer_id.id != False:
                if rec.gs_offer_id.client_id != rec.gs_client_id.id:
                    rec.gs_client_id= rec.gs_offer_id.client_id
                rec.gs_article_id = False
                return {'domain': {'gs_article_id': [('id', 'in', list(x.id for x in rec.gs_offer_id.article_ids))]}}
        