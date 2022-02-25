from odoo import api, fields, models


class PclCheckType(models.Model):
    _name = 'pcl_checktype'
    _description = 'Tipo verifica'

    name = fields.Char(string='Name')
    description = fields.Text(string='Descrizione')
    department_id = fields.Many2one(comodel_name='hr.department', string='Area/Ufficio')
    
    required = fields.Boolean(string='Necessario')
    periodicity = fields.Selection(string='Periodicità', 
        selection=[
            ('M', 'Mensile'), 
            ('S', 'Settimanale'),
            ('A', 'Annuale'),
            ('', 'Non definita'), ] ,
         default='')
    sequence = fields.Integer(string='Ordinamento')
    
    active = fields.Boolean(string = 'active', help = 'active',default=True)
    
    