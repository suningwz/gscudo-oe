# pylint: disable=too-many-lines
from odoo import api, fields, models


class ComunicazioneB8(models.Model):
    _name = "inail_mod3b"
    _description = "Comunicazione Inail modello 3B"

    name = fields.Char(string="Comunicazione", compute="_compute_name", store=True)

    @api.depends("partner_id", "year")
    def _compute_name(self):
        for record in self:
            if record.partner_id:

                record.name = (
                    (record.partner_id.name or "")
                    + " ("
                    + (str(record.year) or "")
                    + ")"
                )
            else:
                record.name = "Non definito"

    active = fields.Boolean(string="Attivo", default=True)
    complete = fields.Boolean(string="Completa", default=False)

    year = fields.Integer(
        string="Anno", default=lambda self: fields.datetime.now().year - 1
    )
    com_id = fields.Char(string="id")
    idAssociazione = fields.Char(string="idAssociazione")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    lavoratoriOccupati31_m = fields.Integer(string="Occupati 30/06 Maschi")
    lavoratoriOccupati31_f = fields.Integer(string="Occupati 30/06 Femmine")

    lavoratoriOccupati32_m = fields.Integer(string="Occupati 31/12 Maschi")
    lavoratoriOccupati32_f = fields.Integer(string="Occupati 31/12 Femmine")
    lavoratoriOccupati = fields.Selection(
        string="Dati forniti dall'azienda",
        selection=[
            ("SI", "SI"),
            ("NO", "NO"),
        ],
    )

    datiSorveglianzaSanitaria44_m = fields.Integer(
        string="Numero totale lavoratori soggetti a sorveglianza sanitaria (M)"
    )
    datiSorveglianzaSanitaria44_f = fields.Integer(
        string="Numero totale lavoratori soggetti a sorveglianza sanitaria (F)"
    )
    datiSorveglianzaSanitaria45_m = fields.Integer(
        string="Numero totale lavoratori visitati con formulazione del giudizio di idoneità nell"
        "anno di riferimento (M)"
    )
    datiSorveglianzaSanitaria45_f = fields.Integer(
        string="Numero totale lavoratori visitati con formulazione del giudizio di idoneità nell"
        "anno di riferimento (F)"
    )
    datiSorveglianzaSanitaria46_m = fields.Integer(
        string="Numero lavoratori idonei (M)"
    )
    datiSorveglianzaSanitaria46_f = fields.Integer(
        string="Numero lavoratori idonei (F)"
    )
    datiSorveglianzaSanitaria41_m = fields.Integer(
        string="Numero lavoratori con idoneità parziali ( temporanee e permanenti con prescrizioni e/o limitazioni ) (M)"
    )
    datiSorveglianzaSanitaria41_f = fields.Integer(
        string="Numero lavoratori con idoneità parziali ( temporanee e permanenti con prescrizioni e/o limitazioni ) (F)"
    )
    datiSorveglianzaSanitaria47_m = fields.Integer(
        string="Numero lavoratori temporaneamente inidonei (M)"
    )
    datiSorveglianzaSanitaria47_f = fields.Integer(
        string="Numero lavoratori temporaneamente inidonei (F)"
    )
    datiSorveglianzaSanitaria48_m = fields.Integer(
        string="Numero lavoratori permanentemente inidonei (M)"
    )
    datiSorveglianzaSanitaria48_f = fields.Integer(
        string="Numero lavoratori permanentemente inidonei (F)"
    )
    # datiSorveglianzaSanitaria26_m = fields.Integer(
    #     string="Numero totale lavoratori soggetti a sorveglianza sanitaria (M)"
    # )
    # datiSorveglianzaSanitaria26_f = fields.Integer(
    #     string="Numero totale lavoratori soggetti a sorveglianza sanitaria (F)"
    # )
    # datiSorveglianzaSanitaria27_m = fields.Integer(
    #     string="Numero totale lavoratori visitati con formulazione del giudizio di idoneità nell"
    #     "anno di riferimento (M)"
    # )
    # datiSorveglianzaSanitaria27_f = fields.Integer(
    #     string="Numero totale lavoratori visitati con formulazione del giudizio di idoneità nell"
    #     "anno di riferimento (F)"
    # )
    # datiSorveglianzaSanitaria28_m = fields.Integer(string="Numero lavoratori idonei (M)")
    # datiSorveglianzaSanitaria28_f = fields.Integer(string="Numero lavoratori idonei (F)")

    # datiSorveglianzaSanitaria41_m = fields.Integer(
    #     string="Numero lavoratori con idoneità parziali ( temporanee e permanenti con prescrizioni e/o limitazioni ) (M)"
    # )
    # datiSorveglianzaSanitaria41_f = fields.Integer(
    #     string="Numero lavoratori con idoneità parziali ( temporanee e permanenti con prescrizioni e/o limitazioni ) (F)"
    # )
    # datiSorveglianzaSanitaria34_m = fields.Integer(
    #     string="Numero lavoratori temporaneamente inidonei (M)"
    # )
    # datiSorveglianzaSanitaria34_f = fields.Integer(
    #     string="Numero lavoratori temporaneamente inidonei (F)"
    # )
    # datiSorveglianzaSanitaria35_m = fields.Integer(
    #     string="Numero lavoratori permanentemente inidonei (M)"
    # )
    # datiSorveglianzaSanitaria35_f = fields.Integer(
    #     string="Numero lavoratori permanentemente inidonei (F)"
    # )

    esposizioneRischiLavorativi1_sogg_m = fields.Integer(
        string="Movimentazione manuale dei carichi Sogg (M)"
    )
    esposizioneRischiLavorativi1_sogg_f = fields.Integer(
        string="Movimentazione manuale dei carichi Sogg (F)"
    )

    esposizioneRischiLavorativi1_visit_m = fields.Integer(
        string="Movimentazione manuale dei carichi Visit (M)"
    )
    esposizioneRischiLavorativi1_visit_f = fields.Integer(
        string="Movimentazione manuale dei carichi Visit (F)"
    )

    esposizioneRischiLavorativi1_ido_m = fields.Integer(
        string="Movimentazione manuale dei carichi Idonei (M)"
    )
    esposizioneRischiLavorativi1_ido_f = fields.Integer(
        string="Movimentazione manuale dei carichi Idonei (F)"
    )

    esposizioneRischiLavorativi1_inido_m = fields.Integer(
        string="Movimentazione manuale dei carichi Inidonei (M)"
    )
    esposizioneRischiLavorativi1_inido_f = fields.Integer(
        string="Movimentazione manuale dei carichi Inidonei (F)"
    )

    esposizioneRischiLavorativi2_sogg_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Sogg (M)"
    )
    esposizioneRischiLavorativi2_sogg_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Sogg (F)"
    )

    esposizioneRischiLavorativi2_visit_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Visit (M)"
    )
    esposizioneRischiLavorativi2_visit_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Visit (F)"
    )

    esposizioneRischiLavorativi2_ido_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Idonei (M)"
    )
    esposizioneRischiLavorativi2_ido_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Idonei (F)"
    )

    esposizioneRischiLavorativi2_inido_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Inidonei (M)"
    )
    esposizioneRischiLavorativi2_inido_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Inidonei (F)"
    )

    esposizioneRischiLavorativi36_sogg_m = fields.Integer(
        string="Rischi Posturali Sogg (M)"
    )
    esposizioneRischiLavorativi36_sogg_f = fields.Integer(
        string="Rischi Posturali Sogg (F)"
    )

    esposizioneRischiLavorativi36_visit_m = fields.Integer(
        string="Rischi Posturali Visit (M)"
    )
    esposizioneRischiLavorativi36_visit_f = fields.Integer(
        string="Rischi Posturali Visit (F)"
    )

    esposizioneRischiLavorativi36_ido_m = fields.Integer(
        string="Rischi Posturali Idonei (M)"
    )
    esposizioneRischiLavorativi36_ido_f = fields.Integer(
        string="Rischi Posturali Idonei (F)"
    )

    esposizioneRischiLavorativi36_inido_m = fields.Integer(
        string="Rischi Posturali Inidonei (M)"
    )
    esposizioneRischiLavorativi36_inido_f = fields.Integer(
        string="Rischi Posturali Inidonei (F)"
    )

    esposizioneRischiLavorativi3_sogg_m = fields.Integer(
        string="Agenti chimici Sogg (M)"
    )
    esposizioneRischiLavorativi3_sogg_f = fields.Integer(
        string="Agenti chimici Sogg (F)"
    )

    esposizioneRischiLavorativi3_visit_m = fields.Integer(
        string="Agenti chimici Visit (M)"
    )
    esposizioneRischiLavorativi3_visit_f = fields.Integer(
        string="Agenti chimici Visit (F)"
    )

    esposizioneRischiLavorativi3_ido_m = fields.Integer(
        string="Agenti chimici Idonei (M)"
    )
    esposizioneRischiLavorativi3_ido_f = fields.Integer(
        string="Agenti chimici Idonei (F)"
    )

    esposizioneRischiLavorativi3_inido_m = fields.Integer(
        string="Agenti chimici Inidonei (M)"
    )
    esposizioneRischiLavorativi3_inido_f = fields.Integer(
        string="Agenti chimici Inidonei (F)"
    )

    esposizioneRischiLavorativi37_sogg_m = fields.Integer(
        string="Agenti cancerogeni Sogg (M)"
    )
    esposizioneRischiLavorativi37_sogg_f = fields.Integer(
        string="Agenti cancerogeni Sogg (F)"
    )

    esposizioneRischiLavorativi37_visit_m = fields.Integer(
        string="Agenti cancerogeni Visit (M)"
    )
    esposizioneRischiLavorativi37_visit_f = fields.Integer(
        string="Agenti cancerogeni Visit (F)"
    )

    esposizioneRischiLavorativi37_ido_m = fields.Integer(
        string="Agenti cancerogeni Idonei (M)"
    )
    esposizioneRischiLavorativi37_ido_f = fields.Integer(
        string="Agenti cancerogeni Idonei (F)"
    )

    esposizioneRischiLavorativi37_inido_m = fields.Integer(
        string="Agenti cancerogeni Inidonei (M)"
    )
    esposizioneRischiLavorativi37_inido_f = fields.Integer(
        string="Agenti cancerogeni Inidonei (F)"
    )

    esposizioneRischiLavorativi38_sogg_m = fields.Integer(
        string="Agenti mutageni Sogg (M)"
    )
    esposizioneRischiLavorativi38_sogg_f = fields.Integer(
        string="Agenti mutageni Sogg (F)"
    )

    esposizioneRischiLavorativi38_visit_m = fields.Integer(
        string="Agenti mutageni Visit (M)"
    )
    esposizioneRischiLavorativi38_visit_f = fields.Integer(
        string="Agenti mutageni Visit (F)"
    )

    esposizioneRischiLavorativi38_ido_m = fields.Integer(
        string="Agenti mutageni Idonei (M)"
    )
    esposizioneRischiLavorativi38_ido_f = fields.Integer(
        string="Agenti mutageni Idonei (F)"
    )

    esposizioneRischiLavorativi38_inido_m = fields.Integer(
        string="Agenti mutageni Inidonei (M)"
    )
    esposizioneRischiLavorativi38_inido_f = fields.Integer(
        string="Agenti mutageni Inidonei (F)"
    )

    esposizioneRischiLavorativi5_sogg_m = fields.Integer(string="Amianto Sogg (M)")
    esposizioneRischiLavorativi5_sogg_f = fields.Integer(string="Amianto Sogg (F)")

    esposizioneRischiLavorativi5_visit_m = fields.Integer(string="Amianto Visit (M)")
    esposizioneRischiLavorativi5_visit_f = fields.Integer(string="Amianto Visit (F)")

    esposizioneRischiLavorativi5_ido_m = fields.Integer(string="Amianto Idonei (M)")
    esposizioneRischiLavorativi5_ido_f = fields.Integer(string="Amianto Idonei (F)")

    esposizioneRischiLavorativi5_inido_m = fields.Integer(string="Amianto Inidonei (M)")
    esposizioneRischiLavorativi5_inido_f = fields.Integer(string="Amianto Inidonei (F)")

    esposizioneRischiLavorativi49_sogg_m = fields.Integer(string="Silice Sogg (M)")
    esposizioneRischiLavorativi49_sogg_f = fields.Integer(string="Silice Sogg (F)")

    esposizioneRischiLavorativi49_visit_m = fields.Integer(string="Silice Visit (M)")
    esposizioneRischiLavorativi49_visit_f = fields.Integer(string="Silice Visit (F)")

    esposizioneRischiLavorativi49_ido_m = fields.Integer(string="Silice Idonei (M)")
    esposizioneRischiLavorativi49_ido_f = fields.Integer(string="Silice Idonei (F)")

    esposizioneRischiLavorativi49_inido_m = fields.Integer(string="Silice Inidonei (M)")
    esposizioneRischiLavorativi49_inido_f = fields.Integer(string="Silice Inidonei (F)")

    esposizioneRischiLavorativi7_sogg_m = fields.Integer(
        string="Agenti biologici Sogg (M)"
    )
    esposizioneRischiLavorativi7_sogg_f = fields.Integer(
        string="Agenti biologici Sogg (F)"
    )

    esposizioneRischiLavorativi7_visit_m = fields.Integer(
        string="Agenti biologici Visit (M)"
    )
    esposizioneRischiLavorativi7_visit_f = fields.Integer(
        string="Agenti biologici Visit (F)"
    )

    esposizioneRischiLavorativi7_ido_m = fields.Integer(
        string="Agenti biologici Idonei (M)"
    )
    esposizioneRischiLavorativi7_ido_f = fields.Integer(
        string="Agenti biologici Idonei (F)"
    )

    esposizioneRischiLavorativi7_inido_m = fields.Integer(
        string="Agenti biologici Inidonei (M)"
    )
    esposizioneRischiLavorativi7_inido_f = fields.Integer(
        string="Agenti biologici Inidonei (F)"
    )

    esposizioneRischiLavorativi8_sogg_m = fields.Integer(
        string="Videoterminali Sogg (M)"
    )
    esposizioneRischiLavorativi8_sogg_f = fields.Integer(
        string="Videoterminali Sogg (F)"
    )

    esposizioneRischiLavorativi8_visit_m = fields.Integer(
        string="Videoterminali Visit (M)"
    )
    esposizioneRischiLavorativi8_visit_f = fields.Integer(
        string="Videoterminali Visit (F)"
    )

    esposizioneRischiLavorativi8_ido_m = fields.Integer(
        string="Videoterminali Idonei (M)"
    )
    esposizioneRischiLavorativi8_ido_f = fields.Integer(
        string="Videoterminali Idonei (F)"
    )

    esposizioneRischiLavorativi8_inido_m = fields.Integer(
        string="Videoterminali Inidonei (M)"
    )
    esposizioneRischiLavorativi8_inido_f = fields.Integer(
        string="Videoterminali Inidonei (F)"
    )

    esposizioneRischiLavorativi9_sogg_m = fields.Integer(
        string="Vibrazioni corpo intero Sogg (M)"
    )
    esposizioneRischiLavorativi9_sogg_f = fields.Integer(
        string="Vibrazioni corpo intero Sogg (F)"
    )

    esposizioneRischiLavorativi9_visit_m = fields.Integer(
        string="Vibrazioni corpo intero Visit (M)"
    )
    esposizioneRischiLavorativi9_visit_f = fields.Integer(
        string="Vibrazioni corpo intero Visit (F)"
    )

    esposizioneRischiLavorativi9_ido_m = fields.Integer(
        string="Vibrazioni corpo intero Idonei (M)"
    )
    esposizioneRischiLavorativi9_ido_f = fields.Integer(
        string="Vibrazioni corpo intero Idonei (F)"
    )

    esposizioneRischiLavorativi9_inido_m = fields.Integer(
        string="Vibrazioni corpo intero Inidonei (M)"
    )
    esposizioneRischiLavorativi9_inido_f = fields.Integer(
        string="Vibrazioni corpo intero Inidonei (F)"
    )

    esposizioneRischiLavorativi10_sogg_m = fields.Integer(
        string="Vibrazioni mano braccio Sogg (M)"
    )
    esposizioneRischiLavorativi10_sogg_f = fields.Integer(
        string="Vibrazioni mano braccio Sogg (F)"
    )

    esposizioneRischiLavorativi10_visit_m = fields.Integer(
        string="Vibrazioni mano braccio Visit (M)"
    )
    esposizioneRischiLavorativi10_visit_f = fields.Integer(
        string="Vibrazioni mano braccio Visit (F)"
    )

    esposizioneRischiLavorativi10_ido_m = fields.Integer(
        string="Vibrazioni mano braccio Idonei (M)"
    )
    esposizioneRischiLavorativi10_ido_f = fields.Integer(
        string="Vibrazioni mano braccio Idonei (F)"
    )

    esposizioneRischiLavorativi10_inido_m = fields.Integer(
        string="Vibrazioni mano braccio Inidonei (M)"
    )
    esposizioneRischiLavorativi10_inido_f = fields.Integer(
        string="Vibrazioni mano braccio Inidonei (F)"
    )

    esposizioneRischiLavorativi11_sogg_m = fields.Integer(string="Rumore Sogg (M)")
    esposizioneRischiLavorativi11_sogg_f = fields.Integer(string="Rumore Sogg (F)")

    esposizioneRischiLavorativi11_visit_m = fields.Integer(string="Rumore Visit (M)")
    esposizioneRischiLavorativi11_visit_f = fields.Integer(string="Rumore Visit (F)")

    esposizioneRischiLavorativi11_ido_m = fields.Integer(string="Rumore Idonei (M)")
    esposizioneRischiLavorativi11_ido_f = fields.Integer(string="Rumore Idonei (F)")

    esposizioneRischiLavorativi11_inido_m = fields.Integer(string="Rumore Inidonei (M)")
    esposizioneRischiLavorativi11_inido_f = fields.Integer(string="Rumore Inidonei (F)")

    esposizioneRischiLavorativi39_sogg_m = fields.Integer(
        string="Campi Elettromagnetici Sogg (M)"
    )
    esposizioneRischiLavorativi39_sogg_f = fields.Integer(
        string="Campi Elettromagnetici Sogg (F)"
    )

    esposizioneRischiLavorativi39_visit_m = fields.Integer(
        string="Campi Elettromagnetici Visit (M)"
    )
    esposizioneRischiLavorativi39_visit_f = fields.Integer(
        string="Campi Elettromagnetici Visit (F)"
    )

    esposizioneRischiLavorativi39_ido_m = fields.Integer(
        string="Campi Elettromagnetici Idonei (M)"
    )
    esposizioneRischiLavorativi39_ido_f = fields.Integer(
        string="Campi Elettromagnetici Idonei (F)"
    )

    esposizioneRischiLavorativi39_inido_m = fields.Integer(
        string="Campi Elettromagnetici Inidonei (M)"
    )
    esposizioneRischiLavorativi39_inido_f = fields.Integer(
        string="Campi Elettromagnetici Inidonei (F)"
    )

    esposizioneRischiLavorativi12_sogg_m = fields.Integer(
        string="Radiazioni ottiche artificiali Sogg (M)"
    )
    esposizioneRischiLavorativi12_sogg_f = fields.Integer(
        string="Radiazioni ottiche artificiali Sogg (F)"
    )

    esposizioneRischiLavorativi12_visit_m = fields.Integer(
        string="Radiazioni ottiche artificiali Visit (M)"
    )
    esposizioneRischiLavorativi12_visit_f = fields.Integer(
        string="Radiazioni ottiche artificiali Visit (F)"
    )

    esposizioneRischiLavorativi12_ido_m = fields.Integer(
        string="Radiazioni ottiche artificiali Idonei (M)"
    )
    esposizioneRischiLavorativi12_ido_f = fields.Integer(
        string="Radiazioni ottiche artificiali Idonei (F)"
    )

    esposizioneRischiLavorativi12_inido_m = fields.Integer(
        string="Radiazioni ottiche artificiali Inidonei (M)"
    )
    esposizioneRischiLavorativi12_inido_f = fields.Integer(
        string="Radiazioni ottiche artificiali Inidonei (F)"
    )

    esposizioneRischiLavorativi13_sogg_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Sogg (M)"
    )
    esposizioneRischiLavorativi13_sogg_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Sogg (F)"
    )

    esposizioneRischiLavorativi13_visit_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Visit (M)"
    )
    esposizioneRischiLavorativi13_visit_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Visit (F)"
    )

    esposizioneRischiLavorativi13_ido_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Idonei (M)"
    )
    esposizioneRischiLavorativi13_ido_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Idonei (F)"
    )

    esposizioneRischiLavorativi13_inido_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Inidonei (M)"
    )
    esposizioneRischiLavorativi13_inido_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Inidonei (F)"
    )

    esposizioneRischiLavorativi14_sogg_m = fields.Integer(
        string="Microclima severo Sogg (M)"
    )
    esposizioneRischiLavorativi14_sogg_f = fields.Integer(
        string="Microclima severo Sogg (F)"
    )

    esposizioneRischiLavorativi14_visit_m = fields.Integer(
        string="Microclima severo Visit (M)"
    )
    esposizioneRischiLavorativi14_visit_f = fields.Integer(
        string="Microclima severo Visit (F)"
    )

    esposizioneRischiLavorativi14_ido_m = fields.Integer(
        string="Microclima severo Idonei (M)"
    )
    esposizioneRischiLavorativi14_ido_f = fields.Integer(
        string="Microclima severo Idonei (F)"
    )

    esposizioneRischiLavorativi14_inido_m = fields.Integer(
        string="Microclima severo Inidonei (M)"
    )
    esposizioneRischiLavorativi14_inido_f = fields.Integer(
        string="Microclima severo Inidonei (F)"
    )

    esposizioneRischiLavorativi40_sogg_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Sogg (M)"
    )
    esposizioneRischiLavorativi40_sogg_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Sogg (F)"
    )

    esposizioneRischiLavorativi40_visit_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Visit (M)"
    )
    esposizioneRischiLavorativi40_visit_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Visit (F)"
    )

    esposizioneRischiLavorativi40_ido_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Idonei (M)"
    )
    esposizioneRischiLavorativi40_ido_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Idonei (F)"
    )

    esposizioneRischiLavorativi40_inido_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Inidonei (M)"
    )
    esposizioneRischiLavorativi40_inido_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Inidonei (F)"
    )

    esposizioneRischiLavorativi21_sogg_m = fields.Integer(
        string="Atmosfere iperbariche Sogg (M)"
    )
    esposizioneRischiLavorativi21_sogg_f = fields.Integer(
        string="Atmosfere iperbariche Sogg (F)"
    )

    esposizioneRischiLavorativi21_visit_m = fields.Integer(
        string="Atmosfere iperbariche Visit (M)"
    )
    esposizioneRischiLavorativi21_visit_f = fields.Integer(
        string="Atmosfere iperbariche Visit (F)"
    )

    esposizioneRischiLavorativi21_ido_m = fields.Integer(
        string="Atmosfere iperbariche Idonei (M)"
    )
    esposizioneRischiLavorativi21_ido_f = fields.Integer(
        string="Atmosfere iperbariche Idonei (F)"
    )

    esposizioneRischiLavorativi21_inido_m = fields.Integer(
        string="Atmosfere iperbariche Inidonei (M)"
    )
    esposizioneRischiLavorativi21_inido_f = fields.Integer(
        string="Atmosfere iperbariche Inidonei (F)"
    )

    esposizioneRischiLavorativi22_sogg_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Sogg (M)"
    )
    esposizioneRischiLavorativi22_sogg_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Sogg (F)"
    )

    esposizioneRischiLavorativi22_visit_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Visit (M)"
    )
    esposizioneRischiLavorativi22_visit_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Visit (F)"
    )

    esposizioneRischiLavorativi22_ido_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Idonei (M)"
    )
    esposizioneRischiLavorativi22_ido_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Idonei (F)"
    )

    esposizioneRischiLavorativi22_inido_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Inidonei (M)"
    )
    esposizioneRischiLavorativi22_inido_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Inidonei (F)"
    )

    esposizioneRischiLavorativi23_sogg_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Sogg (M)"
    )
    esposizioneRischiLavorativi23_sogg_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Sogg (F)"
    )

    esposizioneRischiLavorativi23_visit_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Visit (M)"
    )
    esposizioneRischiLavorativi23_visit_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Visit (F)"
    )

    esposizioneRischiLavorativi23_ido_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Idonei (M)"
    )
    esposizioneRischiLavorativi23_ido_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Idonei (F)"
    )

    esposizioneRischiLavorativi23_inido_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Inidonei (M)"
    )
    esposizioneRischiLavorativi23_inido_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Inidonei (F)"
    )

    esposizioneRischiLavorativi1_sogg_m = fields.Integer(
        string="Movimentazione manuale dei carichi Sogg (M)"
    )
    esposizioneRischiLavorativi1_sogg_f = fields.Integer(
        string="Movimentazione manuale dei carichi Sogg (F)"
    )

    esposizioneRischiLavorativi1_visit_m = fields.Integer(
        string="Movimentazione manuale dei carichi Visit (M)"
    )
    esposizioneRischiLavorativi1_visit_f = fields.Integer(
        string="Movimentazione manuale dei carichi Visit (F)"
    )

    esposizioneRischiLavorativi1_ido_m = fields.Integer(
        string="Movimentazione manuale dei carichi Idonei (M)"
    )
    esposizioneRischiLavorativi1_ido_f = fields.Integer(
        string="Movimentazione manuale dei carichi Idonei (F)"
    )

    esposizioneRischiLavorativi1_inido_m = fields.Integer(
        string="Movimentazione manuale dei carichi Inidonei (M)"
    )
    esposizioneRischiLavorativi1_inido_f = fields.Integer(
        string="Movimentazione manuale dei carichi Inidonei (F)"
    )

    esposizioneRischiLavorativi2_sogg_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Sogg (M)"
    )
    esposizioneRischiLavorativi2_sogg_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Sogg (F)"
    )

    esposizioneRischiLavorativi2_visit_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Visit (M)"
    )
    esposizioneRischiLavorativi2_visit_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Visit (F)"
    )

    esposizioneRischiLavorativi2_ido_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Idonei (M)"
    )
    esposizioneRischiLavorativi2_ido_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Idonei (F)"
    )

    esposizioneRischiLavorativi2_inido_m = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Inidonei (M)"
    )
    esposizioneRischiLavorativi2_inido_f = fields.Integer(
        string="Sovraccarico biomeccanico arti superiori Inidonei (F)"
    )

    esposizioneRischiLavorativi36_sogg_m = fields.Integer(
        string="Rischi Posturali Sogg (M)"
    )
    esposizioneRischiLavorativi36_sogg_f = fields.Integer(
        string="Rischi Posturali Sogg (F)"
    )

    esposizioneRischiLavorativi36_visit_m = fields.Integer(
        string="Rischi Posturali Visit (M)"
    )
    esposizioneRischiLavorativi36_visit_f = fields.Integer(
        string="Rischi Posturali Visit (F)"
    )

    esposizioneRischiLavorativi36_ido_m = fields.Integer(
        string="Rischi Posturali Idonei (M)"
    )
    esposizioneRischiLavorativi36_ido_f = fields.Integer(
        string="Rischi Posturali Idonei (F)"
    )

    esposizioneRischiLavorativi36_inido_m = fields.Integer(
        string="Rischi Posturali Inidonei (M)"
    )
    esposizioneRischiLavorativi36_inido_f = fields.Integer(
        string="Rischi Posturali Inidonei (F)"
    )

    esposizioneRischiLavorativi3_sogg_m = fields.Integer(
        string="Agenti chimici Sogg (M)"
    )
    esposizioneRischiLavorativi3_sogg_f = fields.Integer(
        string="Agenti chimici Sogg (F)"
    )

    esposizioneRischiLavorativi3_visit_m = fields.Integer(
        string="Agenti chimici Visit (M)"
    )
    esposizioneRischiLavorativi3_visit_f = fields.Integer(
        string="Agenti chimici Visit (F)"
    )

    esposizioneRischiLavorativi3_ido_m = fields.Integer(
        string="Agenti chimici Idonei (M)"
    )
    esposizioneRischiLavorativi3_ido_f = fields.Integer(
        string="Agenti chimici Idonei (F)"
    )

    esposizioneRischiLavorativi3_inido_m = fields.Integer(
        string="Agenti chimici Inidonei (M)"
    )
    esposizioneRischiLavorativi3_inido_f = fields.Integer(
        string="Agenti chimici Inidonei (F)"
    )

    esposizioneRischiLavorativi37_sogg_m = fields.Integer(
        string="Agenti cancerogeni Sogg (M)"
    )
    esposizioneRischiLavorativi37_sogg_f = fields.Integer(
        string="Agenti cancerogeni Sogg (F)"
    )

    esposizioneRischiLavorativi37_visit_m = fields.Integer(
        string="Agenti cancerogeni Visit (M)"
    )
    esposizioneRischiLavorativi37_visit_f = fields.Integer(
        string="Agenti cancerogeni Visit (F)"
    )

    esposizioneRischiLavorativi37_ido_m = fields.Integer(
        string="Agenti cancerogeni Idonei (M)"
    )
    esposizioneRischiLavorativi37_ido_f = fields.Integer(
        string="Agenti cancerogeni Idonei (F)"
    )

    esposizioneRischiLavorativi37_inido_m = fields.Integer(
        string="Agenti cancerogeni Inidonei (M)"
    )
    esposizioneRischiLavorativi37_inido_f = fields.Integer(
        string="Agenti cancerogeni Inidonei (F)"
    )

    esposizioneRischiLavorativi38_sogg_m = fields.Integer(
        string="Agenti mutageni Sogg (M)"
    )
    esposizioneRischiLavorativi38_sogg_f = fields.Integer(
        string="Agenti mutageni Sogg (F)"
    )

    esposizioneRischiLavorativi38_visit_m = fields.Integer(
        string="Agenti mutageni Visit (M)"
    )
    esposizioneRischiLavorativi38_visit_f = fields.Integer(
        string="Agenti mutageni Visit (F)"
    )

    esposizioneRischiLavorativi38_ido_m = fields.Integer(
        string="Agenti mutageni Idonei (M)"
    )
    esposizioneRischiLavorativi38_ido_f = fields.Integer(
        string="Agenti mutageni Idonei (F)"
    )

    esposizioneRischiLavorativi38_inido_m = fields.Integer(
        string="Agenti mutageni Inidonei (M)"
    )
    esposizioneRischiLavorativi38_inido_f = fields.Integer(
        string="Agenti mutageni Inidonei (F)"
    )

    esposizioneRischiLavorativi5_sogg_m = fields.Integer(string="Amianto Sogg (M)")
    esposizioneRischiLavorativi5_sogg_f = fields.Integer(string="Amianto Sogg (F)")

    esposizioneRischiLavorativi5_visit_m = fields.Integer(string="Amianto Visit (M)")
    esposizioneRischiLavorativi5_visit_f = fields.Integer(string="Amianto Visit (F)")

    esposizioneRischiLavorativi5_ido_m = fields.Integer(string="Amianto Idonei (M)")
    esposizioneRischiLavorativi5_ido_f = fields.Integer(string="Amianto Idonei (F)")

    esposizioneRischiLavorativi5_inido_m = fields.Integer(string="Amianto Inidonei (M)")
    esposizioneRischiLavorativi5_inido_f = fields.Integer(string="Amianto Inidonei (F)")

    esposizioneRischiLavorativi49_sogg_m = fields.Integer(string="Silice Sogg (M)")
    esposizioneRischiLavorativi49_sogg_f = fields.Integer(string="Silice Sogg (F)")

    esposizioneRischiLavorativi49_visit_m = fields.Integer(string="Silice Visit (M)")
    esposizioneRischiLavorativi49_visit_f = fields.Integer(string="Silice Visit (F)")

    esposizioneRischiLavorativi49_ido_m = fields.Integer(string="Silice Idonei (M)")
    esposizioneRischiLavorativi49_ido_f = fields.Integer(string="Silice Idonei (F)")

    esposizioneRischiLavorativi49_inido_m = fields.Integer(string="Silice Inidonei (M)")
    esposizioneRischiLavorativi49_inido_f = fields.Integer(string="Silice Inidonei (F)")

    esposizioneRischiLavorativi7_sogg_m = fields.Integer(
        string="Agenti biologici Sogg (M)"
    )
    esposizioneRischiLavorativi7_sogg_f = fields.Integer(
        string="Agenti biologici Sogg (F)"
    )

    esposizioneRischiLavorativi7_visit_m = fields.Integer(
        string="Agenti biologici Visit (M)"
    )
    esposizioneRischiLavorativi7_visit_f = fields.Integer(
        string="Agenti biologici Visit (F)"
    )

    esposizioneRischiLavorativi7_ido_m = fields.Integer(
        string="Agenti biologici Idonei (M)"
    )
    esposizioneRischiLavorativi7_ido_f = fields.Integer(
        string="Agenti biologici Idonei (F)"
    )

    esposizioneRischiLavorativi7_inido_m = fields.Integer(
        string="Agenti biologici Inidonei (M)"
    )
    esposizioneRischiLavorativi7_inido_f = fields.Integer(
        string="Agenti biologici Inidonei (F)"
    )

    esposizioneRischiLavorativi8_sogg_m = fields.Integer(
        string="Videoterminali Sogg (M)"
    )
    esposizioneRischiLavorativi8_sogg_f = fields.Integer(
        string="Videoterminali Sogg (F)"
    )

    esposizioneRischiLavorativi8_visit_m = fields.Integer(
        string="Videoterminali Visit (M)"
    )
    esposizioneRischiLavorativi8_visit_f = fields.Integer(
        string="Videoterminali Visit (F)"
    )

    esposizioneRischiLavorativi8_ido_m = fields.Integer(
        string="Videoterminali Idonei (M)"
    )
    esposizioneRischiLavorativi8_ido_f = fields.Integer(
        string="Videoterminali Idonei (F)"
    )

    esposizioneRischiLavorativi8_inido_m = fields.Integer(
        string="Videoterminali Inidonei (M)"
    )
    esposizioneRischiLavorativi8_inido_f = fields.Integer(
        string="Videoterminali Inidonei (F)"
    )

    esposizioneRischiLavorativi9_sogg_m = fields.Integer(
        string="Vibrazioni corpo intero Sogg (M)"
    )
    esposizioneRischiLavorativi9_sogg_f = fields.Integer(
        string="Vibrazioni corpo intero Sogg (F)"
    )

    esposizioneRischiLavorativi9_visit_m = fields.Integer(
        string="Vibrazioni corpo intero Visit (M)"
    )
    esposizioneRischiLavorativi9_visit_f = fields.Integer(
        string="Vibrazioni corpo intero Visit (F)"
    )

    esposizioneRischiLavorativi9_ido_m = fields.Integer(
        string="Vibrazioni corpo intero Idonei (M)"
    )
    esposizioneRischiLavorativi9_ido_f = fields.Integer(
        string="Vibrazioni corpo intero Idonei (F)"
    )

    esposizioneRischiLavorativi9_inido_m = fields.Integer(
        string="Vibrazioni corpo intero Inidonei (M)"
    )
    esposizioneRischiLavorativi9_inido_f = fields.Integer(
        string="Vibrazioni corpo intero Inidonei (F)"
    )

    esposizioneRischiLavorativi10_sogg_m = fields.Integer(
        string="Vibrazioni mano braccio Sogg (M)"
    )
    esposizioneRischiLavorativi10_sogg_f = fields.Integer(
        string="Vibrazioni mano braccio Sogg (F)"
    )

    esposizioneRischiLavorativi10_visit_m = fields.Integer(
        string="Vibrazioni mano braccio Visit (M)"
    )
    esposizioneRischiLavorativi10_visit_f = fields.Integer(
        string="Vibrazioni mano braccio Visit (F)"
    )

    esposizioneRischiLavorativi10_ido_m = fields.Integer(
        string="Vibrazioni mano braccio Idonei (M)"
    )
    esposizioneRischiLavorativi10_ido_f = fields.Integer(
        string="Vibrazioni mano braccio Idonei (F)"
    )

    esposizioneRischiLavorativi10_inido_m = fields.Integer(
        string="Vibrazioni mano braccio Inidonei (M)"
    )
    esposizioneRischiLavorativi10_inido_f = fields.Integer(
        string="Vibrazioni mano braccio Inidonei (F)"
    )

    esposizioneRischiLavorativi11_sogg_m = fields.Integer(string="Rumore Sogg (M)")
    esposizioneRischiLavorativi11_sogg_f = fields.Integer(string="Rumore Sogg (F)")

    esposizioneRischiLavorativi11_visit_m = fields.Integer(string="Rumore Visit (M)")
    esposizioneRischiLavorativi11_visit_f = fields.Integer(string="Rumore Visit (F)")

    esposizioneRischiLavorativi11_ido_m = fields.Integer(string="Rumore Idonei (M)")
    esposizioneRischiLavorativi11_ido_f = fields.Integer(string="Rumore Idonei (F)")

    esposizioneRischiLavorativi11_inido_m = fields.Integer(string="Rumore Inidonei (M)")
    esposizioneRischiLavorativi11_inido_f = fields.Integer(string="Rumore Inidonei (F)")

    esposizioneRischiLavorativi39_sogg_m = fields.Integer(
        string="Campi Elettromagnetici Sogg (M)"
    )
    esposizioneRischiLavorativi39_sogg_f = fields.Integer(
        string="Campi Elettromagnetici Sogg (F)"
    )

    esposizioneRischiLavorativi39_visit_m = fields.Integer(
        string="Campi Elettromagnetici Visit (M)"
    )
    esposizioneRischiLavorativi39_visit_f = fields.Integer(
        string="Campi Elettromagnetici Visit (F)"
    )

    esposizioneRischiLavorativi39_ido_m = fields.Integer(
        string="Campi Elettromagnetici Idonei (M)"
    )
    esposizioneRischiLavorativi39_ido_f = fields.Integer(
        string="Campi Elettromagnetici Idonei (F)"
    )

    esposizioneRischiLavorativi39_inido_m = fields.Integer(
        string="Campi Elettromagnetici Inidonei (M)"
    )
    esposizioneRischiLavorativi39_inido_f = fields.Integer(
        string="Campi Elettromagnetici Inidonei (F)"
    )

    esposizioneRischiLavorativi12_sogg_m = fields.Integer(
        string="Radiazioni ottiche artificiali Sogg (M)"
    )
    esposizioneRischiLavorativi12_sogg_f = fields.Integer(
        string="Radiazioni ottiche artificiali Sogg (F)"
    )

    esposizioneRischiLavorativi12_visit_m = fields.Integer(
        string="Radiazioni ottiche artificiali Visit (M)"
    )
    esposizioneRischiLavorativi12_visit_f = fields.Integer(
        string="Radiazioni ottiche artificiali Visit (F)"
    )

    esposizioneRischiLavorativi12_ido_m = fields.Integer(
        string="Radiazioni ottiche artificiali Idonei (M)"
    )
    esposizioneRischiLavorativi12_ido_f = fields.Integer(
        string="Radiazioni ottiche artificiali Idonei (F)"
    )

    esposizioneRischiLavorativi12_inido_m = fields.Integer(
        string="Radiazioni ottiche artificiali Inidonei (M)"
    )
    esposizioneRischiLavorativi12_inido_f = fields.Integer(
        string="Radiazioni ottiche artificiali Inidonei (F)"
    )

    esposizioneRischiLavorativi13_sogg_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Sogg (M)"
    )
    esposizioneRischiLavorativi13_sogg_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Sogg (F)"
    )

    esposizioneRischiLavorativi13_visit_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Visit (M)"
    )
    esposizioneRischiLavorativi13_visit_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Visit (F)"
    )

    esposizioneRischiLavorativi13_ido_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Idonei (M)"
    )
    esposizioneRischiLavorativi13_ido_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Idonei (F)"
    )

    esposizioneRischiLavorativi13_inido_m = fields.Integer(
        string="Radiazioni ultraviolette naturali Inidonei (M)"
    )
    esposizioneRischiLavorativi13_inido_f = fields.Integer(
        string="Radiazioni ultraviolette naturali Inidonei (F)"
    )

    esposizioneRischiLavorativi14_sogg_m = fields.Integer(
        string="Microclima severo Sogg (M)"
    )
    esposizioneRischiLavorativi14_sogg_f = fields.Integer(
        string="Microclima severo Sogg (F)"
    )

    esposizioneRischiLavorativi14_visit_m = fields.Integer(
        string="Microclima severo Visit (M)"
    )
    esposizioneRischiLavorativi14_visit_f = fields.Integer(
        string="Microclima severo Visit (F)"
    )

    esposizioneRischiLavorativi14_ido_m = fields.Integer(
        string="Microclima severo Idonei (M)"
    )
    esposizioneRischiLavorativi14_ido_f = fields.Integer(
        string="Microclima severo Idonei (F)"
    )

    esposizioneRischiLavorativi14_inido_m = fields.Integer(
        string="Microclima severo Inidonei (M)"
    )
    esposizioneRischiLavorativi14_inido_f = fields.Integer(
        string="Microclima severo Inidonei (F)"
    )

    esposizioneRischiLavorativi40_sogg_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Sogg (M)"
    )
    esposizioneRischiLavorativi40_sogg_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Sogg (F)"
    )

    esposizioneRischiLavorativi40_visit_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Visit (M)"
    )
    esposizioneRischiLavorativi40_visit_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Visit (F)"
    )

    esposizioneRischiLavorativi40_ido_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Idonei (M)"
    )
    esposizioneRischiLavorativi40_ido_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Idonei (F)"
    )

    esposizioneRischiLavorativi40_inido_m = fields.Integer(
        string="Infrasuoni/Ultrasuoni Inidonei (M)"
    )
    esposizioneRischiLavorativi40_inido_f = fields.Integer(
        string="Infrasuoni/Ultrasuoni Inidonei (F)"
    )

    esposizioneRischiLavorativi21_sogg_m = fields.Integer(
        string="Atmosfere iperbariche Sogg (M)"
    )
    esposizioneRischiLavorativi21_sogg_f = fields.Integer(
        string="Atmosfere iperbariche Sogg (F)"
    )

    esposizioneRischiLavorativi21_visit_m = fields.Integer(
        string="Atmosfere iperbariche Visit (M)"
    )
    esposizioneRischiLavorativi21_visit_f = fields.Integer(
        string="Atmosfere iperbariche Visit (F)"
    )

    esposizioneRischiLavorativi21_ido_m = fields.Integer(
        string="Atmosfere iperbariche Idonei (M)"
    )
    esposizioneRischiLavorativi21_ido_f = fields.Integer(
        string="Atmosfere iperbariche Idonei (F)"
    )

    esposizioneRischiLavorativi21_inido_m = fields.Integer(
        string="Atmosfere iperbariche Inidonei (M)"
    )
    esposizioneRischiLavorativi21_inido_f = fields.Integer(
        string="Atmosfere iperbariche Inidonei (F)"
    )

    esposizioneRischiLavorativi22_sogg_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Sogg (M)"
    )
    esposizioneRischiLavorativi22_sogg_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Sogg (F)"
    )

    esposizioneRischiLavorativi22_visit_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Visit (M)"
    )
    esposizioneRischiLavorativi22_visit_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Visit (F)"
    )

    esposizioneRischiLavorativi22_ido_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Idonei (M)"
    )
    esposizioneRischiLavorativi22_ido_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Idonei (F)"
    )

    esposizioneRischiLavorativi22_inido_m = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Inidonei (M)"
    )
    esposizioneRischiLavorativi22_inido_f = fields.Integer(
        string="Lavoro notturno &gt; 80gg/anno Inidonei (F)"
    )

    esposizioneRischiLavorativi23_sogg_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Sogg (M)"
    )
    esposizioneRischiLavorativi23_sogg_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Sogg (F)"
    )

    esposizioneRischiLavorativi23_visit_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Visit (M)"
    )
    esposizioneRischiLavorativi23_visit_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Visit (F)"
    )

    esposizioneRischiLavorativi23_ido_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Idonei (M)"
    )
    esposizioneRischiLavorativi23_ido_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Idonei (F)"
    )

    esposizioneRischiLavorativi23_inido_m = fields.Integer(
        string="Altri rischi evidenziati da V.R. Inidonei (M)"
    )
    esposizioneRischiLavorativi23_inido_f = fields.Integer(
        string="Altri rischi evidenziati da V.R. Inidonei (F)"
    )

    adempimenti42a_m = fields.Integer(
        string="Alcol - N. lav. Controllati nell'anno con test di screening (M)"
    )

    adempimenti42a_f = fields.Integer(
        string="Alcol - N. lav. Controllati nell'anno con test di screening (F)"
    )

    adempimenti42b_m = fields.Integer(
        string="Alcol - N. lavoratori inviati presso SERT o Centro Alcologico (M)"
    )

    adempimenti42b_f = fields.Integer(
        string="Alcol - N. lavoratori inviati presso SERT o Centro Alcologico (F)"
    )

    adempimenti42c_m = fields.Integer(
        string="Alcol - N. casi di dipendenza confermati dal Centro Specialistico (M)"
    )

    adempimenti42c_f = fields.Integer(
        string="Alcol - N. casi di dipendenza confermati dal Centro Specialistico (F)"
    )

    adempimenti43a_m = fields.Integer(
        string="Droghe - N. lav. Controllati nell'anno con test di screening (M)"
    )

    adempimenti43a_f = fields.Integer(
        string="Droghe - N. lav. Controllati nell'anno con test di screening (F)"
    )

    adempimenti43b_m = fields.Integer(
        string="Droghe - N. lavoratori inviati presso SERT o Centro Alcologico (M)"
    )

    adempimenti43b_f = fields.Integer(
        string="Droghe - N. lavoratori inviati presso SERT o Centro Alcologico (F)"
    )

    adempimenti43c_m = fields.Integer(
        string="Droghe - N. casi di dipendenza confermati dal Centro Specialistico (M)"
    )

    adempimenti43c_f = fields.Integer(
        string="Droghe - N. casi di dipendenza confermati dal Centro Specialistico (F)"
    )
