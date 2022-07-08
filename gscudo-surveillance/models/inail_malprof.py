from odoo import _, api, fields, models


class MalattiaProfessionale(models.Model):
    _name = "inail_malprof"
    _description = "Malattia Professionale"

    name = fields.Char(string="Nome", compute="_compute_name", store=True)

    def _compute_name(self):
        for record in self:
            record.name = (
                record.codMalattia
                + " "
                + record.codAgente
                + " "
                + record.codLst
                + " "
                + record.descMalattia
                + " "
                + record.descAgente
                + " "
            )

    cod_malattia = fields.Char(string="Codice", )
    desc_malattia = fields.Char(string="Malattia", )
    cod_gruppo = fields.Char(string="Codice Gruppo", )
    cod_agente = fields.Char(string="Codice Agente", )
    desc_agete = fields.Char(string="Descrizione Agente", )
    cod_lst = fields.Char(string="Codice Lista", )
    active = fields.Boolean(string="Attivo", default=True)
