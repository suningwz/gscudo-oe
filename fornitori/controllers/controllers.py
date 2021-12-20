# -*- coding: utf-8 -*-
# from odoo import http


# class Fornitori(http.Controller):
#     @http.route('/fornitori/fornitori/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/fornitori/fornitori/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('fornitori.listing', {
#             'root': '/fornitori/fornitori',
#             'objects': http.request.env['fornitori.fornitori'].search([]),
#         })

#     @http.route('/fornitori/fornitori/objects/<model("fornitori.fornitori"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('fornitori.object', {
#             'object': obj
#         })
