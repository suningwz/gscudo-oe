from dateutil.relativedelta import relativedelta

from odoo import api, models, fields


class GSMedicalPlanner(models.Model):
    _name = "gs_medical_planner"
    _description = "Pianificatore sorveglianza sanitaria"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Nome", compute="_compute_name", store=True, index=True)

    # Dati cliente
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Cliente", tracking=True, index=True
    )
    sg_esolver_id = fields.Integer(
        related="partner_id.sg_esolver_id", string="ID ESolver"
    )
    employee_number = fields.Integer(
        related="partner_id.employee_number", string="Numero dipendenti"
    )
    city = fields.Char(related="partner_id.city", string="Sede cliente")
    state_id = fields.Many2one(related="partner_id.state_id", string="Provincia")
    pec_address = fields.Char(string="Indirizzo PEC", compute="_compute_pec_address")

    # Dati contratto
    sale_order_id = fields.Many2one(
        comodel_name="sale.order", string="Offerta", tracking=True, index=True
    )
    sale_state = fields.Selection(related="sale_order_id.state", string="Stato offerta")
    contract_start_date = fields.Date(string="Data decorrenza contratto", tracking=True)
    contract_duration = fields.Integer(
        string="Durata contrattuale (mesi)", default=12, tracking=True
    )
    contract_end_date = fields.Date(
        string="Data fine contratto", compute="_compute_contract_end_date", store=True
    )

    # Dati fornitore
    supplier_id = fields.Many2one(
        comodel_name="res.partner", string="Fornitore", tracking=True
    )
    supplier_note = fields.Char(string="Note fornitore")
    main_doctor_id = fields.Many2one(
        related="partner_id.main_doctor_id",
        string="Medico competente",
        store=True,
        index=True,
    )
    other_doctors = fields.Char(related="partner_id.other_doctors")
    doctor_note = fields.Char(string="Note medico")
    assignment_date = fields.Date(string="Data nomina attuale medico", tracking=True)

    # Dati gestione
    date_pec = fields.Date(string="Data PEC sollecito", tracking=True)
    is_nomination_acquired = fields.Boolean(string="Nomina presente", tracking=True)
    nomination_note = fields.Char(string="Note nomina")
    is_data_acquired = fields.Boolean(string="Dati ricevuti", tracking=True)
    is_gs_managed = fields.Boolean(string="Gestito da Gruppo Scudo", tracking=True)

    # Dati fatturazione
    last_visit_invoice_date = fields.Date(
        string="Ultima fatturazione visite", tracking=True
    )
    last_assignment_invoice_date = fields.Date(
        string="Ultima fatturazione incarico", tracking=True
    )

    # Note
    internal_note = fields.Text(string="Note interne")

    old_id = fields.Integer(string="Id vecchio pianificatore")

    @api.depends("partner_id", "contract_start_date", "sale_order_id")
    def _compute_name(self):
        for record in self:
            record.name = " - ".join(
                [
                    record.partner_id.name or "",
                    record.contract_start_date.strftime("%d/%m/%Y")
                    if record.contract_start_date
                    else "",
                    record.sale_order_id.name or "",
                ]
            )

    def _compute_pec_address(self):
        for record in self:
            if record.partner_id.l10n_it_pec_email:
                record.pec_address = record.partner_id.l10n_it_pec_email
            else:
                record.pec_address = record.partner_id.parent_id.l10n_it_pec_email

    @api.depends("contract_start_date", "contract_duration")
    def _compute_contract_end_date(self):
        for record in self:
            if record.contract_start_date and record.contract_duration:
                record.contract_end_date = record.contract_start_date + relativedelta(
                    months=record.contract_duration, days=-1
                )
            else:
                record.contract_end_date = False
