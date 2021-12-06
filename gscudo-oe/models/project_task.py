from odoo import _, api, fields, models


class ProjectProject(models.Model):
    _inherit = 'project.task'

    sg_offer = fields.Char(string='Rif Offerta')
    sg_offer_id = fields.Integer(string='ID Offerta SawGest')
    sg_offer_items_id = fields.Integer(string='ID Riga Offerta SawGest')
    sg_task_id = fields.Integer(string='ID Attività SawGest')
    sg_url = fields.Char(string='Vedi in sawgest' ,compute="_compute_sg_url", store=False )

    def _compute_sg_url(self):
        irconfigparam = self.env['ir.config_parameter']
        base_url = irconfigparam.sudo().get_param('sawgest_base_url')
        if base_url:
            for record in self:
                if record.sg_task_id and record.sg_task_id > 0:
                    record.sg_url = base_url + "tasks/" + str(record.sg_task_id)
                else:
                    record.sg_url = False