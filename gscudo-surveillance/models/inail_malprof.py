from odoo import api, fields, models


class MalattiaProfessionale(models.Model):
    _name = "inail_malprof"
    _description = "Malattia Professionale"

    name = fields.Char(string="Nome", compute="_compute_name", store=True)

    @api.depends(
        "cod_malattia", "cod_agente", "cod_lst", "desc_malattia", "desc_agente"
    )
    def _compute_name(self):
        for record in self:
            record.name = (
                (record.cod_malattia or "")
                + " "
                + (record.cod_agente or "")
                + " "
                + (record.cod_lst or "")
                + " "
                + (record.desc_malattia or "")
                + " "
                + (record.desc_agente or "")
            )

    cod_malattia = fields.Char(
        string="Codice",
    )
    desc_malattia = fields.Char(
        string="Malattia",
    )
    cod_gruppo = fields.Char(
        string="Codice Gruppo",
    )
    cod_agente = fields.Char(
        string="Codice Agente",
    )
    desc_agente = fields.Char(
        string="Descrizione Agente",
    )
    cod_lst = fields.Char(
        string="Codice Lista",
    )
    active = fields.Boolean(string="Attivo", default=True)
