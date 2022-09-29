from odoo import models, fields, api


class GSMessageWizard(models.TransientModel):
    _name = "gs_message_wizard"
    _description = "Wizard visualizzazione messaggi"

    message = fields.Text(string="Messaggio")

    # pylint: disable-next=no-self-use
    def action_ok(self):
        """Close the message window."""
        return {"type": "ir.actions.act_window_close"}

    @api.model
    def display_message(self, title, message):
        """Return the display message action."""
        return {
            "name": title,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "gs_message_wizard",
            "res_id": self.env["gs_message_wizard"].create({"message": message}).id,
            "target": "new",
        }
