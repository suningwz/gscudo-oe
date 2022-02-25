# -*- coding: utf-8 -*-
# from odoo import http


# class Gscudo-kpi(http.Controller):
#     @http.route('/gscudo-kpi/gscudo-kpi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gscudo-kpi/gscudo-kpi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gscudo-kpi.listing', {
#             'root': '/gscudo-kpi/gscudo-kpi',
#             'objects': http.request.env['gscudo-kpi.gscudo-kpi'].search([]),
#         })

#     @http.route('/gscudo-kpi/gscudo-kpi/objects/<model("gscudo-kpi.gscudo-kpi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gscudo-kpi.object', {
#             'object': obj
#         })
