# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.wrappers import Request, Response
import json
import base64

class GsPowerBI(http.Controller):

    def _authenticate_user(self):

        if "HTTP_CLIENT_KEY" in request.httprequest.environ:
            client_key = request.httprequest.environ["HTTP_CLIENT_KEY"]
        elif "HTTP_AUTHORIZATION" in request.httprequest.environ:
            client_key = request.httprequest.environ["HTTP_AUTHORIZATION"]
            if client_key.startswith("Basic "):
                client_key = base64.b64decode(client_key[6:]).decode()
            else:
                client_key = None
        elif "client_key" in request.params:
            client_key = request.params["client_key"]
        else:
            client_key = None

        if client_key:
            username,password=client_key.split(":")
        
            user_id = request.env["res.users"].sudo().search([("login", "=", username)])
            
            if user_id and request.env['res.users.apikeys']._check_credentials(scope='rpc', key=password) == user_id.id:
                return user_id

        raise Exception("Invalid Credentials")


    @http.route("/gscudo-powerbi/query/<query_code>", auth="public", methods=["GET"])
    def query(self, query_code, **kw):
        
        try:
            user=self._authenticate_user()
        except Exception as e:
            return Response(json.dumps({"error":"Invalid Credentials"}),status=401)
             
        gs_powerbi_query = request.env["gs_powerbi_query"].sudo().search([("code", "=", query_code),'|', ('groups_id', '=', False), ('groups_id', 'in', user.groups_id.ids)])
        if gs_powerbi_query:

            request.env.cr.execute(gs_powerbi_query.query,{"uid":user.id })
            res = request.env.cr.dictfetchall()
            return Response(json.dumps(res, default=str), mimetype="application/json")
        else:
            return Response(json.dumps({"error":"Query not found"}),status=404)

    @http.route("/gscudo-powerbi/test", type="http", auth="public")
    def get_data(self, **kw):

        try:
            user=self._authenticate_user()
        except Exception as e:
            return Response(json.dumps({"error":"Invalid Credentials"}),status=401)
        
       
        sql = "SELECT id, login from res_users where id=%(uid)s"
        if "sql" in request.params:
            sql = request.params["sql"]
        request.env.cr.execute(sql,{"uid":user.id })
        res = request.env.cr.dictfetchall()
        return Response(json.dumps(res, default=str), mimetype="application/json")
