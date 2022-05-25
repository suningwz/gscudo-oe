from odoo import models, fields


class GSCourseType(models.Model):
    _name = "gs_course_type"
    _description = "GS Tipo di corso"

    name = fields.Char(string="Tipo di corso", required=True)
    code = fields.Char(string="Codice")

    product_id = fields.Many2one(comodel_name="product.product", string="Prodotto")

    mode = fields.Selection(
        string="Modalità",
        selection=[("P", "Presenza"), ("E", "E-learning"), ("M", "Misto")],
        default="P",
    )
    active = fields.Boolean(string="Attivo", default=True)
    duration = fields.Float(string="Durata in ore", default=2, required=True)
    note = fields.Char(string="Note")
    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type", string="Certificato formativo"
    )
    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Certificato formativo (old)",
    )
    is_update = fields.Boolean(string="È un aggiornamento", default=False)
    is_multicompany = fields.Boolean(string="Multiazendale", default=False)
