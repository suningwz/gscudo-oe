import pytz

from odoo import api, fields, models


class GSTrainingPlanner(models.Model):
    _name = "gs_training_planner"
    _description = "Pianificatore Formazione"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Nome", compute="_compute_name", readonly=True, store=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Cliente",
        tracking=True,
    )
    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Offerta",
        domain="[('partner_id','=', partner_id.id)]",
        tracking=True,
    )
    sale_order_line_id = fields.Many2one(
        comodel_name="sale.order.line",
        string="Riga Offerta",
        domain="[('sale_order_id','=', order_id.id)]",
        tracking=True,
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Prodotto",
        tracking=True,
    )

    @api.onchange("sale_order_line_id")
    def _onchange_sale_order_line_id(self):
        if self.sale_order_line_id:
            self.product_id = self.sale_order_line_id.product_id
            self.price_unit = self.sale_order_line_id.price_unit
            self.product_uom_qty = self.sale_order_line_id.product_uom_qty
            self.discount = self.sale_order_line_id.discount
            self.price_subtotal = self.sale_order_line_id.price_subtotal

    sale_state = fields.Selection(related="sale_order_id.state", string="Stato offerta")

    gs_course_type_id = fields.Many2one(
        comodel_name="gs_course_type",
        string="Tipo di corso",
        tracking=True,
    )

    gs_course_id = fields.Many2one(
        comodel_name="gs_course",
        string="Corso",
        domain="[('gs_course_type_id', '=', gs_course_type_id)]",
        tracking=True,
    )
    gs_training_certificate_type_id = fields.Many2one(
        related="gs_course_id.gs_course_type_id.gs_training_certificate_type_id",
        string="Tipo di certificato formativo",
    )

    sale_order_create_date = fields.Datetime(
        related="sale_order_id.create_date", string="Data Offerta"
    )
    date_order = fields.Datetime(
        related="sale_order_id.date_order", string="Data Conferma"
    )

    currency_id = fields.Many2one(related="sale_order_id.currency_id")
    price_unit = fields.Float(string="Prezzo articolo")
    product_uom_qty = fields.Float(string="Quantità", digits="Product Unit of Measure")
    discount = fields.Float(string="Sconto * 100")
    discount_percent = fields.Float(string="Sconto", compute="_compute_discount_percent")

    def _compute_discount_percent(self):
        for record in self:
            record.discount_percent = record.discount / 100

    price_subtotal = fields.Monetary(string="Totale")

    invoice_ref = fields.Char(string="Fatture", tracking=True)
    creditnote_ref = fields.Char(string="Note Accredito", tracking=True)

    place = fields.Char(string="Luogo", tracking=True)
    is_multicompany = fields.Boolean(
        string="Multiaziendale", tracking=True, default=False
    )
    is_online = fields.Boolean(string="Modalità FAD", tracking=True, default=False)

    is_atcustomer = fields.Boolean(
        string="Presso cliente", tracking=True, default=False
    )

    tutor = fields.Char(string="Fornitore", tracking=True)
    tutor_price = fields.Float(string="Docenza prezzo", tracking=True)
    tutor_order_ref = fields.Char(string="Rif. ordine docente", tracking=True)

    course_start_date = fields.Date(
        related="gs_course_id.start_date", string="Data inizio", store=True
    )
    course_end_date = fields.Date(related="gs_course_id.end_date", string="Data fine")

    lesson_times = fields.Text(string="Orari corso", compute="_compute_lesson_times")

    def _compute_lesson_times(self):
        tz = pytz.timezone(self.env.user.tz)

        def lesson_time(lesson):
            if lesson.start_time is False or lesson.end_time is False:
                return "data da definire"
            return (
                f'{lesson.start_time.astimezone(tz).strftime("%d/%m/%Y %H:%M")} - '
                f'{lesson.end_time.astimezone(tz).strftime("%H:%M")}'
            )

        for record in self:
            record.lesson_times = "\n".join(
                [
                    f"{l.name}: {lesson_time(l)}"
                    for l in self.env["gs_course_lesson"].sorted(
                        record.gs_course_id.gs_course_lesson_ids
                    )
                    if l.generate_certificate is False
                ]
            )

    @api.onchange("gs_course_id")
    def _onchange_gs_course_id(self):
        self._compute_lesson_times()

    place_supplier = fields.Char(string="Fornitore Sala", tracking=True)
    place_price = fields.Float(string="Prezzo Sala", tracking=True)
    place_order_ref = fields.Char(string="Rif. ordine sala", tracking=True)
    material_supplier = fields.Char(string="Fornitore Materali", tracking=True)
    material_price = fields.Float(string="Prezzo Materiali", tracking=True)
    material_order_ref = fields.Char(string="Rif. ordine materiali", tracking=True)

    note = fields.Text(string="Note", tracking=True)

    course_attendants = fields.Integer(string="Partecipanti/Edizioni", tracking=True)
    # tot_qty = fields.Integer(string="Q.tà", tracking=True)
    tot_hours = fields.Float(related="gs_course_id.duration", string="Nr. Ore")
    course_price = fields.Float(string="Prezzo unitario")

    external_url = fields.Char(related="gs_course_id.external_url", string="Url corso")
    sawgest_offer_url = fields.Char(
        related="sale_order_id.sg_url", string="SaWGest Offerta"
    )

    status = fields.Selection(
        [
            ("1-nuovo", "Da gestire"),
            ("2-proposto", "Proposto"),
            ("3-accettato", "Accettato"),
            ("4-in corso", "In corso"),
            ("5-concluso", "Concluso"),
            ("X-annullato", "Annullato"),
        ],
        string="Status",
    )

    @api.depends(
        "sale_order_id.name",
        "gs_course_type_id.name",
        "gs_course_id.protocol",
        "course_start_date",
        "partner_id.name",
    )
    def _compute_name(self):
        for record in self:
            record.name = " - ".join(
                [
                    record.sale_order_id.name or "",
                    record.gs_course_type_id.name or "",
                    record.gs_course_id.protocol if record.gs_course_id else "",
                    record.course_start_date.strftime("%d/%m/%Y")
                    if record.course_start_date
                    else "data da definire",
                    record.partner_id.name or "",
                ]
            ).strip(" -")

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.sale_order_id = False
        self._onchange_sale_order_id()

    @api.onchange("sale_order_id")
    def _onchange_sale_order_id(self):
        self.sale_order_line_id = False

    old_id = fields.Integer(string="Vecchio ID")
