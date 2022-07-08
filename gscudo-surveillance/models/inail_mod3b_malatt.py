from odoo import _, api, fields, models


class InailMod3BMalatt(models.Model):
    _name = 'inail_mod3b_malatt'
    _description = 'Malattie Modello 3b'

    inail_mod3b_id = fields.Many2one(comodel_name='inail_mod3b', string='Modello 3b')
    inail_malprof_id = fields.Many2one(comodel_name='inail_malprof', string='Malattie Professione')
    
    name = fields.Char(string='Malattie',compute='_compute_name',store=True)
    def _compute_name(self):
        for record in self:
            record.name = record.inail_mod3b_id.name + " " + record.inail_malprof_id.name

    numero_maschi  = fields.Integer(string='Maschi')
    numero_femmine = fields.Integer(string='Femmine')

class InailMod3B(models.Model):
    _inherit = 'inail_mod3b'
    inail_mod3b_malatt_ids = fields.One2many(comodel_name='inail_mod3b_malatt', inverse_name='inail_mod3b_id', string='Malattie')