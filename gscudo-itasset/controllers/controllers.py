# -*- coding: utf-8 -*-
# from odoo import http


# class Gscudo-itasset(http.Controller):
#     @http.route('/gscudo-itasset/gscudo-itasset/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gscudo-itasset/gscudo-itasset/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gscudo-itasset.listing', {
#             'root': '/gscudo-itasset/gscudo-itasset',
#             'objects': http.request.env['gscudo-itasset.gscudo-itasset'].search([]),
#         })

#     @http.route('/gscudo-itasset/gscudo-itasset/objects/<model("gscudo-itasset.gscudo-itasset"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gscudo-itasset.object', {
#             'object': obj
#         })
