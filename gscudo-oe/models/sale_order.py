from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = "sale.order"

    product_family_id = fields.Many2one(
        comodel_name="gs_product_family", string="Famiglia"
    )
    sg_offer_id = fields.Integer(string="ID Offerta SaWGest")
    sg_url = fields.Char(
        string="Vedi in SaWGest", compute="_compute_sg_url", store=False
    )

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_offer_id is not False and record.sg_offer_id > 0:
                    record.sg_url = f"{base_url}offers/{record.sg_offer_id}"
                else:
                    record.sg_url = False
