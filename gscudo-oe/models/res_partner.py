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


    position_inail = fields.Char(string='Posizione Inail')
    position_inps = fields.Char(string='Posizione INPS')
    position_cema = fields.Char(string='Posizione CEMA')
    cciaa = fields.Char(string='CCIAA')
    nrea = fields.Char(string='N REA')
    
    revenue = fields.Integer('Fatturato')
    balance_year = fields.Integer(string="Anno bilancio", default='')
    employee_qty = fields.Integer('Adetti')
    #ateco_id = fields.Many2one("ateco.category", string="Descrizione ATECO 2007")
    rating = fields.Integer(string='Rating')
    share_capital = fields.Float(string='Capitale Sociale')
    #credit_limit = fields.Float(string='Fido')
    prejudicials = fields.Boolean(string='Pregiudizievoli')
    
