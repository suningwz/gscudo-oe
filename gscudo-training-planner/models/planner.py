import pytz

from odoo import api, fields, models


class GSTrainingPlanner(models.Model):
    _name = "gs_training_planner"
    _description = "Pianificatore Formazione"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Nome", compute="_compute_name", readonly=True, store=True
    )

    # FIXME enroll workers
    # FIXME enrollment status related (inverse)

    # creation_date = fields.Date(string="Data creazione")

    # field connected to Sawgest data
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
        related="sale_order_line_id.product_id",
        comodel_name="product.product",
        string="Prodotto",
        # domain="[('product_family_id', '=', 'Formazione')]",
        # tracking=True,
    )

    # FIXME sale_order_state

    # TODO domain from product_id
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

    # gs_training_class_id = fields.Many2one(
    #     related="gs_training_class_course_id.training_class_id",
    #     comodel_name="gs_training_classes",
    #     string="Classe",
    # )
    # gs_training_article_id = fields.Many2one(
    #     related="gs_training_class_course_id.article_id",
    #     comodel_name="gs_articles",
    #     string="Argomento",
    # )

    sale_order_create_date = fields.Datetime(
        related="sale_order_id.create_date", string="Data Offerta"
    )
    date_order = fields.Datetime(
        related="sale_order_id.date_order", string="Data Conferma"
    )

    currency_id = fields.Many2one(related="sale_order_id.currency_id")
    price_unit = fields.Float(
        related="sale_order_line_id.price_unit", string="Prezzo articolo"
    )
    product_uom_qty = fields.Float(
        related="sale_order_line_id.product_uom_qty",
        string="Quantità",
        digits="Product Unit of Measure",
    )
    discount = fields.Float(related="sale_order_line_id.discount", string="Sconto")

    price_subtotal = fields.Monetary(
        related="sale_order_line_id.price_subtotal", string="Totale"
    )

    # fields for administrations teams
    invoice_ref = fields.Char(string="Fatture", tracking=True)
    creditnote_ref = fields.Char(string="Note Accredito", tracking=True)

    # fields for training staff teams
    place = fields.Char(string="Luogo", tracking=True)
    is_multicompany = fields.Boolean(
        related="gs_course_id.is_multicompany",
        string="Multiaziendale",
    )
    is_online = fields.Boolean(string="Modalità FAD", compute="_compute_is_online")

    @api.depends("gs_course_id", "gs_course_id.mode")
    def _compute_is_online(self):
        for record in self:
            record.is_online = record.gs_course_id.mode == "E"

    is_atcustomer = fields.Boolean(
        string="Presso cliente", tracking=True, default=False
    )

    # def _compute_is_atcustomer(self):
    #     for _ in self:
    #         pass
    #         # record.is_atcustomer =

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
                    for l in record.gs_course_id.gs_course_lesson_ids
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

    note = fields.Text(string="Note")

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
        ],
        string="Status",
    )

    # FIXME article?
    @api.depends("gs_course_type_id", "course_start_date", "partner_id")
    def _compute_name(self):
        for record in self:
            record.name = " ".join(
                [
                    record.gs_course_type_id.name or "",
                    record.course_start_date.strftime("%d/%m/%Y")
                    if record.course_start_date
                    else "",
                    record.partner_id.name or "",
                ]
            ).strip()

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        self.sale_order_id = False
        self._onchange_sale_order_id()
        # if rec.gs_client_id.id is not False:
        #     if rec.gs_offer_id.client_id.id != rec.gs_client_id.id:
        #         rec.gs_offer_id = False
        # return {
        #     "domain": {
        #         "gs_offer_id": [
        #             ("offer_state_id", "in", [2, 10]),
        #             ("deleted_at", "=", False),
        #             ("client_id", "=", rec.gs_client_id.id),
        #         ]
        #     }
        # }

    @api.onchange("sale_order_id")
    def _onchange_sale_order_id(self):
        self.sale_order_line_id = False
        # if rec.gs_offer_id.id is not False:
        #     if rec.gs_offer_id.client_id.id != rec.gs_client_id.id:
        #         rec.gs_client_id = rec.gs_offer_id.client_id
        #     rec.gs_article_id = False
        # return {
        #     "domain": {
        #         "gs_article_id": [
        #             (
        #                 "id",
        #                 "in",
        #                 list(x.id for x in rec.gs_offer_id.article_ids),
        #             )
        #         ]
        #     }
        # }
