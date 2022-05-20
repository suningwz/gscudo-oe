from odoo import fields, models

# TODO colors
_COLORS = [
    ("white", "Bianco"),
    ("red", "Rosso"),
    ("blue", "Blu"),
    ("green", "Verde"),
    ("yellow", "Giallo"),
    ("grey", "Grigio"),
]


class GSCertificateType(models.Model):
    _name = "gs_certificate_type"
    _description = "Tipo Certificato Formativo"

    name = fields.Char(string="Nome")
    active = fields.Boolean(string="Attivo", default=True)
    code = fields.Char(string="Codice")
    note = fields.Char(string="Note")
    validity_interval = fields.Integer(string="Lunghezza validità in anni")
    is_updateable = fields.Boolean(string="Aggiornabile")
    law_ref = fields.Text(string="Riferimento normativo")

    # Visualization options
    # TODO sequence
    color = fields.Selection(string="Colore", selection=_COLORS)
    visibility = fields.Boolean("Visibilità")

    # some certificates automatically give you other certificates
    gs_certificate_type_ids = fields.Many2many(
        comodel_name="gs_certificate_type",
        relation="gs_certificate_type_rel",
        column1="stronger",
        column2="weaker",
        string="Soddisfa anche",
    )

    def satisfies(self, other):
        """
        Returns True if self is stronger than other
        """
        return other == self or other in self.gs_certificate_type_ids
