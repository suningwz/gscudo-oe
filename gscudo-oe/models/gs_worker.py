from odoo import api, fields, models
from odoo.exceptions import ValidationError


class GSWorker(models.Model):
    _name = "gs_worker"
    _description = "Dipendente"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(
        string="Nominativo",
        compute="_compute_name",
        inverse="_split_name",  # pylint: disable=method-inverse
        store=True,
    )
    active = fields.Boolean(string="Attivo", default=True)
    birth_date = fields.Date(string="Data di nascita")
    birth_place = fields.Char(string="Luogo di nascita")
    birth_country = fields.Char(string="Stato di nascita")
    fiscalcode = fields.Char(string="Codice Fiscale")
    sex = fields.Selection(
        string="Sesso",
        selection=[
            ("M", "Maschio"),
            ("F", "Femmina"),
            ("X", "X"),
        ],
    )
    firstname = fields.Char(string="Nome")
    surname = fields.Char(string="Cognome")
    working_hours = fields.Char(string="Ore di lavoro")
    use_videoterminals = fields.Boolean(string="Usa videoterminali")
    use_company_vehicles = fields.Boolean(string="Usa veicoli aziendali")
    night_job = fields.Boolean(string="Lavoro notturno")
    work_at_height = fields.Boolean(string="Lavoro in quota")
    assumption_date = fields.Date(string="Data assunzione")
    phone_number = fields.Char(string="Telefono")
    email = fields.Char(string="Email")
    note = fields.Char(string="Note")

    cartsan_id = fields.Char(string="ID CartSan")

    sg_worker_id = fields.Integer(string="ID SawGest", index=True)
    sg_updated_at = fields.Datetime(string="Data Aggiornamento SaWGest")
    sg_synched_at = fields.Datetime(string="Data ultima sincronizzazione SaWGest")

    sg_url = fields.Char(
        string="Vedi in sawgest", compute="_compute_sg_url", store=False
    )

    def _compute_sg_url(self):
        irconfigparam = self.env["ir.config_parameter"]
        base_url = irconfigparam.sudo().get_param("sawgest_base_url")
        if base_url:
            for record in self:
                if record.sg_worker_id is not False and record.sg_worker_id > 0:
                    record.sg_url = f"{base_url}workers/{record.sg_worker_id}"
                else:
                    record.sg_url = False

    @api.depends("firstname", "surname")
    def _compute_name(self):
        for record in self:
            record.name = f"{record.surname or ''} {record.firstname or ''}"

    @api.depends("name")
    def _split_name(self):
        for record in self:
            splitted = str(record.name).split()
            # if len(splitted) > 2:
            #     surname = splitted[0]
            #     splitted.pop(0)
            #     if len(surname) < 4:
            #         surname = surname + " " + splitted[0]
            #         splitted.pop(0)
            #     firstname = " ".join(splitted)
            # else:
            #     surname = splitted[0]
            #     firstname = splitted[1]

            if len(splitted) == 2:
                surname = splitted[0]
                firstname = splitted[1]
            elif len(splitted) > 2:
                surname = splitted.pop(0)
                if len(surname) < 4:
                    surname += " " + splitted.pop(0)
                firstname = " ".join(splitted)
            else:
                firstname = ""
                surname = ""

            record.surname = surname
            record.firstname = firstname

    @api.onchange("fiscalcode")
    def _onchange_fiscalcode(self):
        if self.fiscalcode is not False:
            duplicate_workers = self.search(
                [
                    ("fiscalcode", "=", self.fiscalcode),
                    ("id", "!=", self.id if self.id else 0),
                ]
            )

            if duplicate_workers:
                raise ValidationError("Codice fiscale già presente.")
