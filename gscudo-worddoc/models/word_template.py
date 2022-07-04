import logging
from odoo import fields, models


_logger = logging.getLogger(__name__)


class ModuleName(models.Model):
    _name = "word_template"
    _description = "Word Template"

    name = fields.Char(string="Nome modello", required=True)
    code = fields.Char(
        string="Codice del modello",
        required=True,
        help="codice del modello, usa solo lettere,numeri e _  senza spazi",
    )
    _sql_constraints = [
        (
            "code_uniq",
            "UNIQUE (code)",
            "Non ci possono essere due template con lo stesso codice",
        )
    ]
    model = fields.Many2one(
        comodel_name="ir.model", ondelete="cascade", string="Modello", required=True
    )

    active = fields.Boolean(string="Active", default=True)
    template = fields.Binary(string="Template", required=True)

    # def word_doc_test_word(self):
    #     return {"name": "dd", "email": "test@example.com"}

    action_id = fields.Many2one(
        comodel_name="ir.actions.server", string="Server Action"
    )

    def create_action(self):
        """
        Creates a server action for the template, and associates it to the model.
        """
        for record in self:
            action_code = (
                "{'type': 'ir.actions.act_url', "
                f"'url': '/gscudo-worddoc/doc/{record.code}/' + str(record.id),"
                "'target': 'new'}"
            )

            action_data = {
                "name": record.name,
                "model_id": record.model.id,
                "binding_model_id": record.model.id,
                "state": "code",
                "code": f"action={action_code}",
            }
            record.action_id = self.env["ir.actions.server"].create(action_data)

    # @api.model
    # def create(self, vals):
    #     s = super().create(vals)
    #     s.create_action()
    #     return s

    def remove_action(self):
        """
        Deletes the action associated to the template.
        """
        for record in self:
            record.action_id.unlink()
