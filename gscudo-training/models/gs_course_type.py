from odoo import models, fields


class GSCourseType(models.Model):
    _name = "gs_course_type"
    _description = "Tipo di corso"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Tipo di corso", required=True, tracking=True)
    code = fields.Char(string="Codice", tracking=True)

    product_id = fields.Many2one(
        comodel_name="product.product", string="Prodotto", tracking=True
    )

    mode = fields.Selection(
        string="Modalità",
        selection=[("P", "Presenza"), ("E", "E-learning"), ("M", "Misto")],
        default="P",
        tracking=True,
    )
    active = fields.Boolean(string="Attivo", default=True)
    duration = fields.Float(string="Durata in ore", default=2, required=True)
    max_workers = fields.Integer(string="Massimo iscritti", default=35, tracking=True)
    min_attendance = fields.Float(
        string="Partecipazione minima", required=True, default=0.9, tracking=True
    )

    content = fields.Text(string="Contenuto")

    note = fields.Char(string="Note")
    gs_training_certificate_type_id = fields.Many2one(
        comodel_name="gs_training_certificate_type",
        string="Certificato formativo",
        tracking=True,
    )

    is_update = fields.Boolean(
        string="È un aggiornamento", default=False, tracking=True
    )
    is_multicompany = fields.Boolean(
        string="Multiazendale", default=False, tracking=True
    )

    is_internal = fields.Boolean(
        string="Corso gestito",
        help=(
            "Decide se l'attestato è generato da Odoo o importato esternamente. "
            "Esempi di corsi non interni sono i corsi AiFOS e quelli organizzati da "
            "Officina del Carrello."
        ),
        default=True,
        tracking=True,
    )

    document_template_id = fields.Many2one(
        comodel_name="word_template",
        string="Modello attestato",
        default=lambda self: (
            self.env["word_template"].search(
                [("code", "ilike", "default_certificate_template")],
                limit=1,
            )
            or False
        ),
        domain=[("model.model", "=", "gs_worker_certificate")],
    )
