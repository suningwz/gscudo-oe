from datetime import date
from math import floor
from odoo import fields, models, api


class GSVisitScheduler(models.Model):
    _name = "gs_visit_scheduler"
    _description = "Scheduler visite"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome")
    agent_id = fields.Many2one(comodel_name="hr.employee", string="Agente")

    technician_id = fields.Many2one(comodel_name="hr.employee", string="Tecnico")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Sede",
    )

    area = fields.Char(string="Area")
    yearly_visits = fields.Integer(string="Visite annuali")
    theoretical_visits = fields.Integer(
        string="Visite teoriche in base a ingresso", compute="_compute_computed_visits"
    )

    @api.depends()
    def _compute_computed_visits(self):
        this_year = date.today().year
        for scheduler in self:
            if scheduler.date_ins.year < this_year:
                scheduler.theoretical_visits = scheduler.yearly_visits
            else:
                days_elapsed = date.today() - date(day=1, month=1, year=this_year)
                scheduler.theoretical_visits = floor(
                    scheduler.yearly_visits * days_elapsed.days / 365
                )

    visit_ids = fields.One2many(
        comodel_name="gs_visit",
        inverse_name="visit_scheduler_id",
        string="Visite",
    )
    total_visits = fields.Integer(
        string="Visite effettuate", compute="_compute_total_visits"
    )

    @api.depends("visit_ids")
    def _compute_total_visits(self):
        for scheduler in self:
            scheduler.total_visits = len(
                [
                    visit
                    for visit in scheduler.visit_ids
                    if visit.date.year == date.today().year
                ]
            )

    assignment = fields.Selection(
        string="Incarico",
        selection=[
            ("rspp", "RSPP"),
            ("odv", "ODV"),
            ("haccp", "HACCP"),
            ("doc", "Documentale"),
            ("ass", "Assistenza"),
            ("ass_v", "Assistenza Vacaz."),
        ],
    )

    date_ins = fields.Date(string="Data Inserimento")
    rspp = fields.Many2one(comodel_name="hr.employee", string="RSPP")
    date_appointment = fields.Date(string="Data Nomina")
    is_appointment_ok = fields.Boolean(string="Nomina ok")

    # expired_documentation =

    note = fields.Char(string="Note")

    non_conformity_number = fields.Integer(string="ID non conformità")
    non_conformity_cause = fields.Integer(string="Causa non conformità")
    non_conformity_correction = fields.Char(string="Correzione non conformità")

    contract_number = fields.Char(string="Contratto")

    ateco_category_id = fields.Many2one(
        comodel_name="ateco.category",
        string="Ateco 2007",
    )

    # Macrosettore Ateco 2006
    # Formazione asr2011
    # Visite teoriche in base a ingresso
