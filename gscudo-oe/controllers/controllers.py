# -*- coding: utf-8 -*-
# from odoo import http


# class ../addons/working/sawgestOdoo/gscudo-oe(http.Controller):
#     @http.route('/gscudo-oe/gscudo-oe/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gscudo-oe/gscudo-oe/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gscudo-oe.listing', {
#             'root': '/gscudo-oe/gscudo-oe',
#             'objects': http.request.env['gscudo-oe.gscudo-oe'].search([]),
#         })

#     @http.route('/gscudo-oe/gscudo-oe/objects/<model("gscudo-oe.gscudo-oe"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gscudo-oe.object', {
#             'object': obj
#         })
