# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.wrappers import Request, Response
import json


class GsPowerBI(http.Controller):
    @http.route("/gscudo-powerbi/gscudo-powerbi/", auth="public")
    def index(self, **kw):
        return "Hello, world"


    @http.route("/gscudo-powerbi/get_data", type="http", auth="user")
    def get_data(self, **kw):

        if "sql" in request.params:
            sql = request.params["sql"]
        request.env.cr.execute(sql)
        res = request.env.cr.dictfetchall()
        return Response(json.dumps(res, default=str), mimetype="application/json")
