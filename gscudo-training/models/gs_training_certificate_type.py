from odoo import fields, models


class GSTrainingCertificateType(models.Model):
    _name = "gs_training_certificate_type"
    _description = "Tipo Certificato Formativo"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome", tracking=True)
    active = fields.Boolean(string="Attivo", default=True, tracking=True)
    code = fields.Char(string="Codice", tracking=True)
    note = fields.Char(string="Note", tracking=True)

    validity_interval = fields.Integer(
        string="Lunghezza validità in anni", tracking=True
    )
    is_updateable = fields.Boolean(string="Aggiornabile", tracking=True)
    law_ref = fields.Text(string="Riferimento normativo", tracking=True)

    # some certificates automatically give you other certificates
    weaker_certificate_ids = fields.Many2many(
        comodel_name="gs_training_certificate_type",
        relation="gs_training_certificate_type_rel",
        column1="stronger",
        column2="weaker",
        string="Certificati implicati",
    )

    stronger_certificate_ids = fields.Many2many(
        comodel_name="gs_training_certificate_type",
        relation="gs_training_certificate_type_rel",
        column1="weaker",
        column2="stronger",
        string="Implicato da",
    )

    is_multicert = fields.Boolean(string="Multicertificato", default=False)
    generates_multicert = fields.Boolean(string="Genera più certificati", default=False)

    def weaker_certificates(self):
        """
        Returns the list of weaker certificate types
        """
        return list(self.weaker_certificate_ids) + [self]
