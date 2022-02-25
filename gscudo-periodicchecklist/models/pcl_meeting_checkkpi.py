from odoo import api, fields, models


class PclMeetingCheckKpi(models.Model):
    _name = 'pcl_meeting_checkkpi'
    _description = 'KPI verifica'

    name = fields.Char(string='Name')
    pcl_meeting_check_id = fields.Many2one(comodel_name="pcl_meeting_check", string="Verifica")
    pcl_checktype_id = fields.Many2one(related="pcl_meeting_check_id.pcl_checktype_id", comodel_name='pcl_checktype', string='Tipo Verifica')
    pcl_checktype_kpi_id =  fields.Many2one(comodel_name='pcl_checktype_kpi', string='Kpi')
    
    kpi_value = fields.Float(string='Valore')
    note = fields.Text(string="Annotazioni")
    

class PclMeetingCheck(models.Model):
    _inherit="pcl_meeting_check"

    pcl_meeting_ckeckkpi_ids  = fields.One2many(comodel_name='pcl_meeting_checkkpi', inverse_name='pcl_meeting_check_id', string='KPIs')
    