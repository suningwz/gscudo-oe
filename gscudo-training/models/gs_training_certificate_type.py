from odoo import fields, models


class CertificateTypeOld(models.Model):
    _name = "gs_training_certificate_type"
    _description = "Tipo Certificato Formativo (old)"

    name = fields.Char(string="Name")
    active = fields.Boolean(string="Attivo", default=True)
    code = fields.Char(string="Codice")
    note = fields.Char(string="Note")
    renewal_interval = fields.Integer(string="Intervallo rinnovo in anni")
    update_interval = fields.Integer(string="Intervallo aggiornamento in anni")
    law_ref = fields.Text(string="Riferimento normativo")
