# -*- coding: utf-8 -*-
# from odoo import http


# class Gscudo-surveillance(http.Controller):
#     @http.route('/gscudo-surveillance/gscudo-surveillance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gscudo-surveillance/gscudo-surveillance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gscudo-surveillance.listing', {
#             'root': '/gscudo-surveillance/gscudo-surveillance',
#             'objects': http.request.env['gscudo-surveillance.gscudo-surveillance'].search([]),
#         })

#     @http.route('/gscudo-surveillance/gscudo-surveillance/objects/<model("gscudo-surveillance.gscudo-surveillance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gscudo-surveillance.object', {
#             'object': obj
#         })
