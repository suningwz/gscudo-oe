from odoo import api, fields, models


class Planner(models.Model):
    _name = "gstraining_planner"
    _description = "Pianificatore Formazione"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Nome", compute="_compute_name", readonly=True, store=True
    )

    creation_date = fields.Date(string="Data creazione")

    # field connected to Sawgest data
    gs_client_id = fields.Many2one(
        comodel_name="gs_clients",
        string="Cliente",
        tracking=True,
    )
    gs_offer_id = fields.Many2one(
        comodel_name="gs_offers",
        string="Offerta",
        domain="[('client_id','=', gs_client_id)]",
        tracking=True,
    )
    gs_offer_items_id = fields.Many2one(
        comodel_name="gs_offer_items",
        string="Riga Offerta",
        domain="[('offer_id','=', gs_offer_id)]",
        tracking=True,
    )
    gs_article_id = fields.Many2one(
        comodel_name="gs_articles",
        string="Articolo",
        tracking=True,
    )
    gs_training_class_course_id = fields.Many2one(
        comodel_name="gs_training_class_courses",
        string="Corso",
        tracking=True,
    )

    gs_training_class_id = fields.Many2one(
        related="gs_training_class_course_id.training_class_id",
        comodel_name="gs_training_classes",
        string="Classe",
    )
    gs_training_article_id = fields.Many2one(
        related="gs_training_class_course_id.article_id",
        comodel_name="gs_articles",
        string="Argomento",
    )

    gs_offer_issue_date = fields.Date(
        related="gs_offer_id.issue_date", string="Data Offerta"
    )
    gs_offer_confirm_date = fields.Datetime(
        related="gs_offer_id.confirm_date", string="Data Conferma"
    )
    gs_offer_article_price = fields.Float(
        string="Prezzo articolo", compute="_compute_article_price", store=True
    )
    gs_offer_article_quantity = fields.Float(
        string="Quantità", compute="_compute_article_price", store=True
    )
    gs_offer_article_discount = fields.Float(
        string="Sconto", compute="_compute_article_price", store=True
    )

    course_total_price = fields.Float(
        string="Totale", compute="_compute_course_total_price"
    )

    @api.depends("gs_offer_id", "gs_article_id")
    def _compute_article_price(self):
        for record in self:
            article_id = record.gs_article_id.id or record.gs_training_article_id.id
            if record.gs_offer_id.id != False and article_id != False:
                self.env.cr.execute(
                    "select article_price,article_quantity,article_discount from gs_offer_article_associations where offer_id = {} and article_id={}".format(
                        record.gs_offer_id.id, article_id
                    )
                )
                oa_list = self.env.cr.fetchall()
                if len(oa_list) == 0:
                    continue
                record.gs_offer_article_price = oa_list[0][0]
                record.gs_offer_article_quantity = oa_list[0][1]
                record.gs_offer_article_discount = oa_list[0][2]
            else:
                record.gs_offer_article_price = 0
                record.gs_offer_article_quantity = 0
                record.gs_offer_article_discount = 0

    def _compute_course_total_price(self):
        for record in self:
            record.course_total_price = (
                record.gs_offer_article_price - record.gs_offer_article_discount
            ) * record.gs_offer_article_quantity

    # fields for administrations teams
    invoice_ref = fields.Char(
        string="Fatture",
        tracking=True,
    )
    creditnote_ref = fields.Char(
        string="Note Accredito",
        tracking=True,
    )
    # fields for training staff teams
    place = fields.Char(
        string="Luogo",
        tracking=True,
    )
    is_multicompany = fields.Boolean(
        string="Multiaziendale", tracking=True, default=False
    )
    is_online = fields.Boolean(string="Modalità FAD", tracking=True, default=False)
    is_atcustomer = fields.Boolean(
        string="Presso cliente", tracking=True, default=False
    )

    tutor = fields.Char(
        string="Fornitore",
        tracking=True,
    )
    tutor_price = fields.Float(
        string="Docenza prezzo",
        tracking=True,
    )
    tutor_order_ref = fields.Char(
        string="Rif. ordine docente",
        tracking=True,
    )

    course_date = fields.Date(
        string="Data",
        tracking=True,
    )
    lesson_dates = fields.Char(
        string="Date corso",
        tracking=True,
    )
    lesson_times = fields.Char(
        string="Orari corso",
        tracking=True,
    )

    place_supplier = fields.Char(
        string="Fornitore Sala",
        tracking=True,
    )
    place_price = fields.Float(
        string="Prezzo Sala",
        tracking=True,
    )
    place_order_ref = fields.Char(
        string="Rif. ordine sala",
        tracking=True,
    )
    material_supplier = fields.Char(
        string="Fornitore Materali",
        tracking=True,
    )
    material_price = fields.Float(
        string="Prezzo Materiali",
        tracking=True,
    )
    material_order_ref = fields.Char(
        string="Rif. ordine materiali",
        tracking=True,
    )

    note = fields.Text(
        string="Note",
    )

    course_attendants = fields.Integer(
        string="Partecipanti/Edizioni",
        tracking=True,
    )
    tot_qty = fields.Integer(
        string="Q.tà",
        tracking=True,
    )
    tot_hours = fields.Float(
        string="Nr. Ore",
        tracking=True,
    )
    course_price = fields.Float(string="Prezzo unitario")

    sawgest_url = fields.Char(
        string="SaWGest Corso", compute="_compute_sawgest_url", store=False
    )

    # @api.onchange('gs_training_class_id')
    def _compute_sawgest_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        for record in self:
            record.sawgest_url = ""
            if record.gs_training_class_id.id:
                record.sawgest_url = (
                    base_url + "training_classes/" + str(record.gs_training_class_id.id)
                )

    sawgest_offer_url = fields.Char(
        string="SaWGest Offerta", compute="_compute_sawgest_offer_url", store=False
    )

    # @api.onchange('gs_offer_id')
    def _compute_sawgest_offer_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        for record in self:
            record.sawgest_offer_url = ""
            if record.gs_offer_id.id:
                record.sawgest_offer_url = (
                    base_url + "offers/" + str(record.gs_offer_id.id)
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

    @api.depends("gs_article_id", "course_date", "gs_client_id")
    def _compute_name(self):
        for record in self:
            record.name = "{} {} {}".format(
                record.gs_article_id.name or "",
                record.course_date or "",
                record.gs_client_id.business_name or "",
            ).strip()

    @api.onchange("gs_client_id")
    def onchange_client_id(self):
        for rec in self:
            if rec.gs_client_id.id != False:
                if rec.gs_offer_id.client_id.id != rec.gs_client_id.id:
                    rec.gs_offer_id = False
                return {
                    "domain": {
                        "gs_offer_id": [
                            ("offer_state_id", "in", [2, 10]),
                            ("deleted_at", "=", False),
                            ("client_id", "=", rec.gs_client_id.id),
                        ]
                    }
                }

    @api.onchange("gs_offer_id")
    def onchange_gs_offer_id(self):
        for rec in self:
            if rec.gs_offer_id.id != False:
                if rec.gs_offer_id.client_id.id != rec.gs_client_id.id:
                    rec.gs_client_id = rec.gs_offer_id.client_id
                rec.gs_article_id = False
                return {
                    "domain": {
                        "gs_article_id": [
                            (
                                "id",
                                "in",
                                list(x.id for x in rec.gs_offer_id.article_ids),
                            )
                        ]
                    }
                }

    @api.onchange("gs_training_class_course_id")
    def onchange_gs_training_class_course_id(self):
        for record in self:
            if record.gs_training_class_course_id.id == False:
                continue
            sql = """
            set time zone 'Europe/Rome';
select  
	gtt.client_id,
	gtt.offer_id,
	tc.article_id ,
	tc.id,
	tc.protocol,
	to_char(min(gtcm2.module_date) at time zone 'UTC','YYYY-MM-DD') course_date,
	count(gtcm2.module_date),
	string_agg(
		distinct 
			to_char(gtcm2.module_date at time zone 'UTC','DD/MM/YY'),' - ' order by 
			to_char(gtcm2.module_date at time zone 'UTC','DD/MM/YY')
			) course_dates,
	string_agg(
		distinct concat(
			to_char(gtcm2.module_date at time zone 'UTC','DD/MM/YY'), ' '),'  ' order by concat(
			to_char(gtcm2.module_date at time zone 'UTC','DD/MM/YY'), ' '
			)) lesson_dates,
	string_agg(
		distinct concat(
			trim(to_char(gtcm2.start_hour,'00')),':', trim(to_char(gtcm2.start_minute,'00')), '-',
			trim(to_char(gtcm2.end_hour,'00')),':', trim(to_char(gtcm2.end_minute,'00'))
			),' / ' order by concat(
			trim(to_char(gtcm2.start_hour,'00')),':', trim(to_char(gtcm2.start_minute,'00')), '-',
			trim(to_char(gtcm2.end_hour,'00')),':', trim(to_char(gtcm2.end_minute,'00'))
			)) lesson_times
	,avg(gtcm2.duration_hour + gtcm2.duration_minute /60) duration
--t.offer_id, gtt.client_id , gc.id, gtt.client_business_name , gc.business_name ,tc.protocol ,  ga.id ,ga."name" 
--gtcm2.code ,gtcm2."name" ,gtcm2.module_date, gtcm2.start_hour 
from gs_training_class_courses tc left outer join gs_training_timetables gtt on gtt.training_class_course_id = tc.id
	inner join gs_training_courses_modules gtcm on gtcm.training_class_course_id =tc.id
	inner join gs_training_class_modules gtcm2 on gtcm.training_class_module_id = gtcm2.id 
	inner  join gs_articles ga on tc.article_id =ga.id
	left outer join gs_offers gof on gof.id = gtt.offer_id 
	--inner join gs_clients gc on gc.id = gtt.client_id 
where 
    tc.id = {}
group by gtt.client_id,
	gtt.offer_id,
	tc.article_id ,
	tc.id,
	tc.protocol
	--gc.business_name 
 ;
            """.format(
                record.gs_training_class_course_id.id
            )
            # print(sql)
            self.env.cr.execute(sql)
            courses = self.env.cr.fetchall()
            if len(courses) == 0:
                record.course_date = False
                record.lesson_dates = False
                record.lesson_times = False
                record.tot_hours = False
            else:
                # print(courses[0][5],courses[0][7])
                record.course_date = courses[0][5]
                record.lesson_dates = courses[0][7]
                record.lesson_times = courses[0][9]
                record.tot_hours = courses[0][10]
