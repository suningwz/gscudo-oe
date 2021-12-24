#-*- coding: utf-8 -*-
from odoo import http


class GsPortal(http.Controller):
    @http.route('/gscudo-portal/gscudo-portal/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/gscudo-portal/gscudo-portal/gs_worker/', auth='public')
    def list(self, **kw):
        return http.request.render('gscudo-oe.gs_worker_view_tree', {
            'root': '/gscudo-portal/gscudo-portal',
            'objects': http.request.env['gs_workers'].search([]),
        })

    @http.route('/gscudo-portal/gscudo-portal/gs_worker/<model("gs_worker"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('gs_worker', {
            'object': obj
        })
