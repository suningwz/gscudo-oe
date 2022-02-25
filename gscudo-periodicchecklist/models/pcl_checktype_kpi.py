from odoo import api, fields, models


class PclCheckTypeKpi(models.Model):
    _name = 'pcl_checktype_kpi'
    _description = 'Kpi Tipo verifica'

    name = fields.Char(string='Kpi')
    plc_checktype_id = fields.Many2one(comodel_name='pcl_checktype', string='Tipo Verifica')
    description = fields.Text(string='Descrizione')
    sequence = fields.Integer(string='Ordinamento')
    active = fields.Boolean(string = 'active', help = 'active',default=True)
    

class PclCheckType(models.Model):

    _inherit="pcl_checktype"

    pcl_checktype_kpi_ids = fields.One2many(comodel_name='pcl_checktype_kpi', inverse_name='plc_checktype_id', string='KPIs')
    