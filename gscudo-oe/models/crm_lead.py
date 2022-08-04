# from datetime import datetime
import re
from odoo import api, fields, models
from odoo.exceptions import ValidationError

COMPETITOR_TYPE = [
    ("", "Non definito"),
    ("int", "Interno"),
    ("est", "Esterno"),
    ("cli", "Cliente"),
]


class CrmLead(models.Model):
    _inherit = "crm.lead"

    _sql_constraints = [("vat", "unique(vat)", "P.IVA già presente")]

    sg_clients_id = fields.Integer(string="ID Cliente SaWGest")
    sg_branches_id = fields.Integer(string="ID Ufficio SaWGest ")
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")

    sg_url = fields.Char(
        string="Vedi in SaWGest", compute="_compute_sg_url", store=False
    )

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_branches_url")
        if base_url:
            for record in self:
                if record.sg_branches_id is not False and record.sg_branches_id > 0:
                    record.sg_url = base_url.format(record.sg_branches_id)
                else:
                    record.sg_url = False

    sg_offers_url = fields.Char(
        string="Offerte in sawgest", compute="_compute_sg_offers_url", store=False
    )

    def _compute_sg_offers_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_clients_id is not False and record.sg_clients_id > 0:
                    record.sg_offers_url = (
                        base_url + f"offers/0/list?cfr={record.sg_clients_id}"
                    )
                else:
                    record.sg_offers_url = False

    fiscalcode = fields.Char(string="Fiscal Code", size=16, help="Italian Fiscal Code")
    pec = fields.Char(string="Addressee PEC")

    tmk_user_id = fields.Many2one(
        comodel_name="res.users", string="Telemarketing operator", tracking=True, index=True,
    )
    gs_partner_division_id = fields.Many2one(
        comodel_name="gs_partner_division", string="Division", tracking=True, index=True,
    )

    position_inail = fields.Char(string="Posizione INAIL")
    position_inps = fields.Char(string="Posizione INPS")
    position_cema = fields.Char(string="Posizione CEMA")

    cciaa = fields.Char(string="CCIAA")
    nrea = fields.Char(string="N REA")

    revenue = fields.Integer(string="Fatturato")
    balance_year = fields.Integer(string="Anno bilancio", default="")
    employee_qty = fields.Integer(string="Addetti")
    ateco_id = fields.Many2one(
        string="Descrizione ATECO 2007", comodel_name="ateco.category",
    )
    rating = fields.Integer(string="Rating")
    share_capital = fields.Float(string="Capitale Sociale")
    credit_limit = fields.Float(string="Fido")
    prejudicials = fields.Boolean(string="Pregiudizievoli")

    ##### Competitors
    # def COMPETITOR_TYPE(self):
    #     return [
    #         ("", "non definito "),
    #         ("int", "interno "),
    #         ("est", "esterno "),
    #         ("cli", "cliente"),
    #     ]

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
        tracking=True, index=True,
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
        tracking=True, index=True,
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
        tracking=True, index=True,
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
        tracking=True, index=True,
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
        tracking=True, index=True,
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
        tracking=True, index=True,
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
        tracking=True, index=True,
    )

    has_competitors = fields.Boolean(
        string="Ci sono concorrenti", compute="_compute_has_competitor", store=True
    )
    is_customer = fields.Boolean(
        string="È cliente", compute="_compute_has_competitor", store=True
    )

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

    @api.constrains("vat", "country_id")
    def _check_vat_ita(self):
        for record in self:
            if record.country_id.code is False or record.country_id.code == "IT":
                if record.vat != "" and record.vat is not False:
                    if re.fullmatch(r"(IT)[0-9]{11}", record.vat) is None:
                        raise ValidationError("Partita Iva non valida")

    @api.depends("user_id")
    def _onchange_user_id(self):
        for record in self:
            if record.user_id is not False:
                if record.user_id.tmk_user_id is not False:
                    record.tmk_user_id = record.user_id.tmk_user_id.id
