from odoo import models, fields, api

COMPETITOR_TYPE = [
    ("", "Non definito"),
    ("int", "Interno"),
    ("est", "Esterno"),
    ("cli", "Cliente"),
]


class ResPartner(models.Model):
    _inherit = "res.partner"

    sg_closed_at = fields.Datetime(string="Chiusura su SG")
    sg_clients_id = fields.Integer(string="ID Cliente SaWGest", index=True)
    sg_branches_id = fields.Integer(string="ID Ufficio SaWGest ", index=True)
    sg_employee_id = fields.Integer(string="ID Impiegato SaWGest", index=True)
    sg_esolver_id = fields.Integer(string="ID ESolver", index=True)
    cartsan_uo_id = fields.Integer(string="ID Cartsan Un. Operativa", index=True)
    cartsan_doc_id = fields.Integer(string="ID Cartsan Medico", index=True)
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima Syncronizzazione SaWGest")
    sg_url = fields.Char(
        string="Vedi in SaWGest", compute="_compute_sg_url", store=False
    )
    sg_note = fields.Text(string="Note Sawgest")

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_branches_url")
        if base_url:
            for record in self:
                if record.sg_branches_id is not False and record.sg_branches_id > 0:
                    record.sg_url = base_url.format(record.sg_branches_id)
                else:
                    record.sg_url = False

    tmk_user_id = fields.Many2one(
        comodel_name="res.users", string="Telemarketing operator", index=True
    )
    gs_partner_division_id = fields.Many2one(
        comodel_name="gs_partner_division", string="Division", index=True
    )

    revenue = fields.Integer(string="Fatturato")
    balance_year = fields.Integer(string="Anno bilancio", default="")
    employee_qty = fields.Integer(string="Addetti")
    main_ateco_id = fields.Many2one(
        comodel_name="ateco.category", string="Descrizione ATECO 2007", index=True
    )
    rating = fields.Integer(string="Rating")
    share_capital = fields.Float(string="Capitale Sociale")
    # credit_limit = fields.Float(string='Fido')
    prejudicials = fields.Boolean(string="Pregiudizievoli")
    split_payment = fields.Boolean(string="Split payment")

    #### From SAWGest

    solicitor = fields.Char(string="Legale Rappresentante")
    employer = fields.Char(string="Datore di lavoro")

    privacy_policy = fields.Boolean(string="Privacy policy")
    marketing_consent = fields.Boolean(string="Marketing consent")

    position_inail = fields.Char(string="Posizione INAIL")
    position_inps = fields.Char(string="Posizione INPS")
    position_cema = fields.Char(string="Posizione CEMA")
    cciaa = fields.Char(string="CCIAA")
    nrea = fields.Char(string="N REA")
    cdc_notes = fields.Text(string="Note cdc")
    required_cig = fields.Boolean(string="Richiesto CIG")
    cig = fields.Char(string="CIG")

    technical_contact = fields.Char(string="Ref. Tecnico")
    technical_contact_notes = fields.Text(string="Ref. Tecnico Note")
    technical_contact_email = fields.Char(string="technical_contact_email")
    technical_contact_phone = fields.Char(string="technical_contact_phone")

    administrative_contact = fields.Char(string="Contatto Amministrativo")
    administrative_contact_notes = fields.Text(string="Contatto Amministrativo Note")
    administrative_contact_email = fields.Char(string="administrative_contact_email")
    administrative_contact_phone = fields.Char(string="administrative_contact_phone")

    employee_number = fields.Integer(string="N. Impiegati")
    main_branch = fields.Boolean(string="Sede principale")

    rspp = fields.Char(string="Nominativo RSPP")
    rspp_notes = fields.Text(string="RSPP Note")
    rls = fields.Char(string="RLS")
    fire_officer = fields.Char(string="Resp. Antincedio")
    prevention_managers_number = fields.Integer(string="Numero Addetti")
    managers_number = fields.Integer(string="Nr Dirigenti")
    fire_officers_number = fields.Integer(string="Nr Addetti Antincendio")
    first_aid_attendants_number = fields.Integer(string="Nr Addetti Primo Soccorso")
    evacuation_coordinators_number = fields.Integer(string="Nr Addetti Evacuazione")
    main_doctor_id = fields.Many2one(comodel_name="res.partner", string="Medico coordinatore")
    other_doctors = fields.Char(string="Medici coordinati")
    doctor = fields.Char(string="Medico")
    doctor_notes = fields.Text(string="Medico Note")
    spring_code = fields.Char(string="spring_code")
    medical_supplier = fields.Char(string="Fornitore Sorveglianza Sanitaria")
    construction_site = fields.Boolean(string="construction_site")

    is_saleagent = fields.Boolean(string="Agente", default=False)
    is_telemarketer = fields.Boolean(string="Telemarketer", default=False)
    is_competitor = fields.Boolean(string="È un competitor", default=False)
    is_frontoffice = fields.Boolean(string="È Frontoffice", default=False)
    is_backoffice = fields.Boolean(string="È Backoffice", default=False)

    safety_competitor_type = fields.Selection(
        string="Sicurezza gestione",
        selection=COMPETITOR_TYPE,
        default="",
        # required=True,
        tracking=True,
    )
    safety_partner_id = fields.Many2one(
        string="Conc. Sicurezza",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    training_competitor_type = fields.Selection(
        string="Formazione gestione",
        selection=COMPETITOR_TYPE,
        default="",
        # required=True,
        tracking=True,
    )
    training_partner_id = fields.Many2one(
        string="Conc. Formazione",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    food_competitor_type = fields.Selection(
        string="Alimentare gestione",
        selection=COMPETITOR_TYPE,
        # required=True,
        default="",
        tracking=True,
    )
    food_partner_id = fields.Many2one(
        string="Conc. Alimentare",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    machdir_competitor_type = fields.Selection(
        string="Dirett. Macchine gestione",
        selection=COMPETITOR_TYPE,
        # required=True,
        default="",
        tracking=True,
    )
    machdir_partner_id = fields.Many2one(
        string="Conc. Dirett. Macchine",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    healthsurv_competitor_type = fields.Selection(
        string="Sorv. Sanit. gestione",
        selection=COMPETITOR_TYPE,
        # required=True,
        default="",
        tracking=True,
    )
    healthsurv_partner_id = fields.Many2one(
        string="Conc. Sorv. Sanit.",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    environment_competitor_type = fields.Selection(
        string="Ambientale gestione",
        selection=COMPETITOR_TYPE,
        # required=True,
        default="",
        tracking=True,
    )
    environment_partner_id = fields.Many2one(
        string="Conc. Ambientale",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    management_competitor_type = fields.Selection(
        string="Sistemi Gest. gestione",
        selection=COMPETITOR_TYPE,
        # required=True,
        default="",
        tracking=True,
    )
    management_partner_id = fields.Many2one(
        string="Conc. Sistemi Gest.",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
        index=True,
    )

    has_competitors = fields.Boolean(
        string="Ci sono concorrenti", compute="_compute_has_competitor", store=True
    )
    is_customer = fields.Boolean(
        string="È cliente", compute="_compute_has_competitor", store=True
    )

    has_safety = fields.Boolean(string="RSPP/Supporto RSPP", default=False)
    has_training_manager = fields.Boolean(string="Manager Formativo", default=False)
    has_healthsurv = fields.Boolean(string="Sorveglianza Sanitaria", default=False)

    @api.depends(
        "safety_competitor_type",
        "training_competitor_type",
        "food_competitor_type",
        "machdir_competitor_type",
        "healthsurv_competitor_type",
        "environment_competitor_type",
    )
    def _compute_has_competitor(self):
        for record in self:
            record.has_competitors = False
            record.is_customer = False

            if (
                record.safety_competitor_type == "est"
                or record.training_competitor_type == "est"
                or record.food_competitor_type == "est"
                or record.machdir_competitor_type == "est"
                or record.healthsurv_competitor_type == "est"
                or record.environment_competitor_type == "est"
            ):
                record.has_competitors = True

            if (
                record.safety_competitor_type == "cli"
                or record.training_competitor_type == "cli"
                or record.food_competitor_type == "cli"
                or record.machdir_competitor_type == "cli"
                or record.healthsurv_competitor_type == "cli"
                or record.environment_competitor_type == "cli"
            ):
                record.is_customer = True

    @api.depends("user_id")
    def _onchange_user_id(self):
        for record in self:
            if record.user_id is not False:
                if record.user_id.tmk_user_id is not False:
                    record.tmk_user_id = record.user_id.tmk_user_id.id
