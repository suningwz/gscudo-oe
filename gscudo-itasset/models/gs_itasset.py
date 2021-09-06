# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ItAsset(models.Model):
    _name = 'gs_itasset'
    _description = 'Assets per la gestione dell''IT e dei dipendenti'
    _inherit = ['mail.thread', 
                'mail.activity.mixin']

    name = fields.Char(string="Cespite",  tracking=True)
    description = fields.Char(string="Descrizione", tracking=True)
    active = fields.Boolean(string='Attivo', default=True, tracking=True)
    serial = fields.Char(string='Numero di serie', tracking=True)
    accounting_ref = fields.Char(string='Rf. Contabile', tracking=True)
    status = fields.Selection(string='Stato', selection=[('1', 'buono'),
                                                         ('2', 'mediocre'),
                                                         ('3', 'guasto/riparabile'),
                                                         ('4', 'guasto/obsoleto'),
                                                         ('9', 'non reperibile')], tracking=True)

    parent_id = fields.Many2one(
        comodel_name='gs_itasset', string='Collegato / installato su', tracking=True)
    children_ids = fields.One2many(
        comodel_name='gs_itasset', inverse_name='parent_id', string='Collegati')

    itasset_location = fields.Selection(string='Sede', selection=[(
        'UD', 'Udine'), ('PN', 'Pordenone'), ('TO', 'Tolmezzo'), ('CO', 'Cordenons')], tracking=True)
    itasset_type_id = fields.Many2one(
        comodel_name='gs_itasset_type', string='Tipologia',  tracking=True)
    itasset_type_family = fields.Char(
        string='Categoria', related='itasset_type_id.family', readonly=True)
    employee_id = fields.Many2one(
        comodel_name='hr.employee', string='Assegnatario',  tracking=True)
    department = fields.Char(
        string='Ufficio', related='employee_id.department_id.name', readonly=True)
    note = fields.Text(string='Annotazioni')
    acquisition_date = fields.Date(string='Data acquisizione')
    expiration_date = fields.Date(string='Data scadenza')
    
    

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        for record in self:
            for asset_id in record.children_ids:
                asset_id.write(
                    {'employee_id': record.employee_id.id}
                )
