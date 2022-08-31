# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PowerbiQuery(models.Model):
    _name = 'gs_powerbi_query'
    _description = 'Query PowerBi'

    name = fields.Char(string="Name", required=True)
    code = fields.Char(string='Codice', required=True)

    query = fields.Text(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    groups_id = fields.Many2many('res.groups', string='Groups',
                                 help="If you have groups, the visibility of this query will be based on these groups. "\
                                      "If this field is empty, this query will be visible to all user.")
    