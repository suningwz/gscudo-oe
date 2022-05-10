# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from collections import OrderedDict
from operator import itemgetter

from odoo import http, _
from odoo.exceptions import AccessError, MissingError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.tools import groupby as groupbyelem

from odoo.osv.expression import OR


class GscudoPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'workers_count' in counters:
            values['workers_count'] = request.env['gs_worker'].search_count([])
       
        return values

    # ------------------------------------------------------------
    # My Worker
    # ------------------------------------------------------------
    def _worker_get_page_view_values(self, worker, access_token, **kwargs):
        values = {
            'page_name': 'worker',
            'worker': worker,
        }
        return self._get_page_view_values(worker, access_token, values, 'my_workers_history', False, **kwargs)

    @http.route(['/my/workers', '/my/workers/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_workerss(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        Worker = request.env['gs_worker']
        domain = []

        searchbar_sortings = {
            'date': {'label': _('Newest'), 'order': 'contract_start_date desc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'name'
        order = searchbar_sortings[sortby]['order']

        if date_begin and date_end:
            domain += [('contract_start_date', '>', date_begin), ('contract_start_date', '<=', date_end)]

        # workers count
        workers_count = Worker.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/workers",
            url_args={'contract_start_date': date_begin, 'contract_end_date': date_end, 'sortby': sortby},
            total=workers_count,
            page=page,
            step=self._items_per_page
        )

        # content according to pager and archive selected
        workers = Worker.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        request.session['my_workers_history'] = workers.ids[:100]

        values.update({
            'contract_start_date': date_begin,
            'contract_end_date': date_end,
            'gs_workers': workers,
            'page_name': 'worker',
            'default_url': '/my/workers',
            'pager': pager,
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby
        })
        return request.render("gscudo-portal.portal_my_workers", values)

    @http.route(['/my/worker/<int:worker_id>'], type='http', auth="public", website=True)
    def portal_my_worker(self, worker_id=None, access_token=None, **kw):
        try:
            worker_sudo = self._document_check_access('gs_worker', worker_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        values = self._worker_get_page_view_values(worker_sudo, access_token, **kw)
        return request.render("gscudo-portal.portal_my_worker", values)

    @http.route(['/my/worker_update/<int:worker_id>'], type='http', auth="user",csrf=False,website=True)
    def portal_worker_update(self, worker_id=None, access_token=None, **kw):

        try:
            worker_sudo = self._document_check_access('gs_worker', worker_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        worker = request.env['gs_worker'].browse(worker_id)
        worker.write({'surname':kw['surname'],})

        values = self._worker_get_page_view_values(worker_sudo, access_token, **kw)
        return request.redirect('/my/worker/%s' % worker_id)
