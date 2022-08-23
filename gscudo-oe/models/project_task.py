from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    sg_offer = fields.Char(string="Rif Offerta")
    sg_offer_id = fields.Integer(string="ID Offerta SaWGest")
    sg_offer_item_id = fields.Integer(string="ID Riga Offerta SaWGest")
    sg_task_id = fields.Integer(string="ID Attività SaWGest")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")
    sg_url = fields.Char(string="Vedi in SaWGest", compute="_compute_sg_url", store=False)

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_task_id is not False and record.sg_task_id > 0:
                    # record.sg_url = f"{base_url}tasks/{str(record.sg_task_id)}"
                    record.sg_url = f"{base_url}tasks/{record.sg_task_id}"
                else:
                    record.sg_url = False

    sg_offer_url = fields.Char(string="Vedi Offerta in SaWGest", compute="_compute_sg_offer_url", store=False)

    def _compute_sg_offer_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_offer_id is not False and record.sg_offer_id > 0:
                    record.sg_offer_url = f"{base_url}offers/{record.sg_offer_id}"
                else:
                    record.sg_offer_url = False

    tmk_user_id = fields.Many2one(
        comodel_name="res.users", string="Telemarketing operator", compute="_compute_tmk_user_id", store=False)
    def _compute_tmk_user_id(self):
        for record in self:
            if record.partner_id:
                record.tmk_user_id = record.partner_id.tmk_user_id.id
            else:
                record.tmk_user_id = record.project_id.partner_id.tmk_user_id.id
            