from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    sg_order_items_id  = fields.Integer('ID order_items Sawgest')
    sg_products_id  = fields.Integer('ID products Sawgest')
    sg_articles_id  = fields.Integer('ID products Sawgest')
    