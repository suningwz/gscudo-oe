from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    sg_offer = fields.Char(string="Rif Offerta")
    sg_offer_id = fields.Integer(string="ID Offerta SaWGest")
    sg_offer_items_id = fields.Integer(string="ID Riga Offerta SaWGest")
    sg_task_id = fields.Integer(string="ID Attività SaWGest")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")
    sg_url = fields.Char(
        string="Vedi in SaWGest", compute="_compute_sg_url", store=False
    )

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

    