# -*- coding: utf-8 -*-
from odoo import models, fields, api

COMPETITOR_TYPE = [
    ("", "Non definito"),
    ("int", "Interno"),
    ("est", "Esterno"),
    ("cli", "Cliente"),
]

class ResPartner(models.Model):
    _inherit = "res.partner"

    sg_clients_id = fields.Integer(string="ID Cliente SaWGest")
    sg_branches_id = fields.Integer(string="ID Ufficio SaWGest ")
    sg_employee_id = fields.Integer(string="ID Impiegato SaWGest")
    sg_esolver_id = fields.Integer(string="ID ESolver")
    cartsan_uo_id = fields.Integer(string="ID Cartsan Un. Operativa")
    cartsan_doc_id = fields.Integer(string="ID Cartsan Medico")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima Syncronizzazione SaWGest")
    sg_url = fields.Char(
        string="Vedi in SaWGest", compute="_compute_sg_url", store=False
    )

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_branches_url")
        if base_url:
            for record in self:
                if record.sg_branches_id and record.sg_branches_id > 0:
                    record.sg_url = base_url.format(record.sg_branches_id)
                else:
                    record.sg_url = False

    tmk_user_id = fields.Many2one(
        comodel_name="res.users", string="Telemarketing operator"
    )
    gs_partner_division_id = fields.Many2one(
        comodel_name="gs_partner_division", string="Division"
    )

    revenue = fields.Integer(string="Fatturato")
    balance_year = fields.Integer(string="Anno bilancio", default="")
    employee_qty = fields.Integer(String="Adetti")
    main_ateco_id = fields.Many2one(comodel_name="ateco.category", string="Descrizione ATECO 2007")
    rating = fields.Integer(string="Rating")
    share_capital = fields.Float(string="Capitale Sociale")
    # credit_limit = fields.Float(string='Fido')
    prejudicials = fields.Boolean(string="Pregiudizievoli")

    #### From SAWGest

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

    rspp = fields.Char(string="Nominativo RSPP")
    rspp_notes = fields.Text(string="RSPP Note")
    rls = fields.Char(string="RLS")
    fire_officer = fields.Char(string="Resp. Antincedio")
    prevention_managers_number = fields.Integer(string="Numero Addetti ")
    managers_number = fields.Integer(string="Nr Dirigenti")
    fire_officers_number = fields.Integer(string="Nr Addetti Antincendio")
    first_aid_attendants_number = fields.Integer(string="Nr Addetti Primo Soccorso")
    evacuation_coordinators_number = fields.Integer(string="Nr Addetti Evacuazione")
    doctor = fields.Char(string="Medico")
    doctor_notes = fields.Text(string="Medico Note")
    spring_code = fields.Char(string="spring_code")
    medical_supplier = fields.Char(string="Fornitore Sorveglianza Sanitaria")

    is_saleagent = fields.Boolean(string="Agente", default=False)
    is_telemarketer = fields.Boolean(string="Telemarketer", default=False)
    is_competitor = fields.Boolean(string="È un competitor", default=False)
    is_frontoffice = fields.Boolean(string="È Frontoffice", default=False)
    is_backoffice = fields.Boolean(string="È Backoffice", default=False)

    ##### Competitors
    def get_competitor_type(self):
        return [
            ("", "non definito "),
            ("int", "interno "),
            ("est", "esterno "),
            ("cli", "cliente"),
        ]

    safety_competitor_type = fields.Selection(
        get_competitor_type, string="Sicurezza gestione", default="", tracking=True
    )
    safety_partner_id = fields.Many2one(
        string="Conc. Sicurezza",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    training_competitor_type = fields.Selection(
        get_competitor_type, string="Formazione gestione", default="", tracking=True
    )
    training_partner_id = fields.Many2one(
        string="Conc. Formazione",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    food_competitor_type = fields.Selection(
        get_competitor_type, string="Alimentare gestione", default="", tracking=True
    )
    food_partner_id = fields.Many2one(
        string="Conc. Alimentare",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    machdir_competitor_type = fields.Selection(
        get_competitor_type,
        string="Dirett. Macchine gestione",
        default="",
        tracking=True,
    )
    machdir_partner_id = fields.Many2one(
        string="Conc. Dirett. Macchine",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    healthsurv_competitor_type = fields.Selection(
        get_competitor_type, string="Sorv. Sanit. gestione", default="", tracking=True
    )
    healthsurv_partner_id = fields.Many2one(
        string="Conc. Sorv. Sanit.",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    environment_competitor_type = fields.Selection(
        get_competitor_type, string="Ambientale gestione", default="", tracking=True
    )
    environment_partner_id = fields.Many2one(
        string="Conc. Ambientale",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    management_competitor_type = fields.Selection(
        get_competitor_type, string="Sistemi Gest. gestione", default="", tracking=True
    )
    management_partner_id = fields.Many2one(
        string="Conc. Sistemi Gest.",
        comodel_name="res.partner",
        domain="[('is_competitor','=',True)]",
        tracking=True,
    )

    has_competitors = fields.Boolean(
        string="Ci sono concorrenti", compute="_compute_has_competitor", store=True
    )
    is_customer = fields.Boolean(
        string="E' cliente", compute="_compute_has_competitor", store=True
    )

    has_safety = fields.Boolean(string="RSPP / Suporto RSPP", default=False)
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
            if record.user_id != False:
                if record.user_id.tmk_user_id != False:
                    record.tmk_user_id = record.user_id.tmk_user_id.id
