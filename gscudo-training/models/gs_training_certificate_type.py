from odoo import fields, models


class GSTrainingCertificateType(models.Model):
    _name = "gs_training_certificate_type"
    _description = "Tipo Certificato Formativo"

    name = fields.Char(string="Nome")
    active = fields.Boolean(string="Attivo", default=True)
    code = fields.Char(string="Codice")
    note = fields.Char(string="Note")

    validity_interval = fields.Integer(string="Lunghezza validità in anni")
    is_updateable = fields.Boolean(string="Aggiornabile")
    law_ref = fields.Text(string="Riferimento normativo")

    # some certificates automatically give you other certificates
    # gs_certificate_type_ids = fields.Many2many(
    weaker_certificate_ids = fields.Many2many(
        comodel_name="gs_training_certificate_type",
        relation="gs_training_certificate_type_rel",
        column1="stronger",
        column2="weaker",
        string="Soddisfa anche",
    )

    def weaker_certificates(self):
        """
        Returns the list of weaker certificate types
        """
        return list(self.weaker_certificate_ids) + [self]
