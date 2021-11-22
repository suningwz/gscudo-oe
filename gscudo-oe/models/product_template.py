from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_family_id = fields.Many2one(comodel_name='gs_product_family', string='Famiglia')
    law_reference = fields.Char(string='Riferimento normativo')
    

    sg_product_id = fields.Integer(string='ID articolo SawGest')
    sg_url = fields.Char(string='Vedi in sawgest' ,compute="_compute_sg_url", store=False )

    

    def _compute_sg_url(self):
        irconfigparam = self.env['ir.config_parameter']
        base_url = irconfigparam.sudo().get_param('sawgest_base_url')
        if base_url:
            for record in self:
                if record.sg_product_id and record.sg_product_id > 0:
                    record.sg_url = base_url+"articles/{}".format(record.sg_product_id)    
                else:
                    record.sg_url = False