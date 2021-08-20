from odoo import api, fields, models


class ITAssetType(models.Model):
    _name = 'gs_itasset_type'
    _description = 'Tipo di asset'

    name = fields.Char(string='Tipo Asset')
    active = fields.Boolean(string='Attivo' , default= True)    
