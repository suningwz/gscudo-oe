from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_family_id = fields.Many2one(
        comodel_name="gs_product_family", string="Famiglia"
    )
    law_reference = fields.Char(string="Riferimento normativo")

    sg_product_id = fields.Integer(string="ID prodotto SaWGest")
    sg_product_url = fields.Char(
        string="Vedi prodotto in SaWGest",
        compute="_compute_sg_product_url",
        store=False,
    )

    def _compute_sg_product_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_product_id is not False and record.sg_product_id > 0:
                    record.sg_product_url = f"{base_url}products/{record.sg_product_id}"
                else:
                    record.sg_product_url = False

    sg_article_id = fields.Integer(string="ID articolo SaWGest")
    sg_article_url = fields.Char(
        string="Vedi articolo in SaWGest",
        compute="_compute_sg_article_url",
        store=False,
    )

    def _compute_sg_article_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_article_id is not False and record.sg_article_id > 0:
                    record.sg_article_url = f"{base_url}articles/{record.sg_article_id}"
                else:
                    record.sg_article_url = False

    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")
