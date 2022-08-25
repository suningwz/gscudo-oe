from odoo import models, fields


class GSMessageWizard(models.TransientModel):
    _name = "gs_message_wizard"
    _description = "Wizard visualizzazione messaggi"

    message = fields.Text(string="Messaggio")

    # pylint: disable-next=no-self-use
    def action_ok(self):
        """Close the message window."""
        return {"type": "ir.actions.act_window_close"}
