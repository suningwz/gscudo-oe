from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    department_id = fields.Many2one(comodel_name="hr.department", string="Dipartimento", index=True,)
    product_family_id = fields.Many2one(
        comodel_name="gs_product_family", string="Famiglia", index=True,
    )

    sg_offer = fields.Char(string="Rif Offerta")
    sg_offer_id = fields.Integer(string="ID Offerta SaWGest")
    sg_url = fields.Char(
        string="Vedi in SaWGest", compute="_compute_sg_url", store=False
    )

    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_offers_url")
        if base_url:
            for record in self:
                if record.sg_offer_id is not False and record.sg_offer_id > 0:
                    record.sg_url = base_url.format(record.sg_offer_id)
                else:
                    record.sg_url = False
