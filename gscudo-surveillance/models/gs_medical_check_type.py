from odoo import fields, models


class MedicalCheckType(models.Model):
    _name = "gs_medical_check_type"
    _description = "Visita / Controllo"

    name = fields.Char(string="Nome")
    active = fields.Boolean(string="Attivo", default=True)
    gs_medical_check_type_id = fields.Many2one(
        comodel_name="gs_medical_check_type", string="Visita / Esame"
    )
    gs_medical_check_frequency_id = fields.Many2one(
        comodel_name="gs_medical_check_frequency", string="Frequenza"
    )
