# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class Partner (models.Model):
    _inherit='res.partner'
    
    sg_clients_id  = fields.Integer(string='ID Cliente SaWGest')
    sg_branches_id = fields.Integer(string='ID Ufficio SaWGest')
    sg_employee_id = fields.Integer(string='ID Impiegato SaWGest')
    

    sg_url = fields.Char(string='Vedi in sawgest' ,compute="_compute_sg_url", store=False )

    
    def _compute_sg_url(self):
        irconfigparam = self.env['ir.config_parameter']
        base_url = irconfigparam.sudo().get_param('sawgest_branches_url')
        if base_url:
            for record in self:
                if record.sg_branches_id > 0:
                    record.sg_url = base_url.format(record.sg_branches_id)    
                else:
                    record.sg_url = False