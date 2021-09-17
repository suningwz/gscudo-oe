# -*- coding: utf-8 -*-
# from odoo import http


# class Gscudo-training(http.Controller):
#     @http.route('/gscudo-training/gscudo-training/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gscudo-training/gscudo-training/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gscudo-training.listing', {
#             'root': '/gscudo-training/gscudo-training',
#             'objects': http.request.env['gscudo-training.gscudo-training'].search([]),
#         })

#     @http.route('/gscudo-training/gscudo-training/objects/<model("gscudo-training.gscudo-training"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gscudo-training.object', {
#             'object': obj
#         })
