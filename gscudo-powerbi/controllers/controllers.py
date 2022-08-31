# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from werkzeug.wrappers import Request, Response
import json


class GsPowerBI(http.Controller):

    def _authenticate_user(self):
        if "HTTP_CLIENT_KEY" in request.httprequest.environ  :
            client_key =request.httprequest.environ["HTTP_CLIENT_KEY"]
       
        if "client_key" in request.params:
            client_key = request.params["client_key"]   
       
        if client_key:
            username,password=client_key.split(":")
        
            user_id = request.env["res.users"].sudo().search([("login", "=", username)])
            
            if user_id and request.env['res.users.apikeys']._check_credentials(scope='rpc', key=password) == user_id.id:
              
                # user_id._check_credentials(password,{"interactive":False})
                # http.request.session.uid = user_id.id
                # http.request.session.login = user_id.login
                # http.request.session.password = user_id.password
                # http.request.session.get_context()
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

    @http.route("/gscudo-powerbi/get_data", type="http", auth="public")
    def get_data(self, **kw):

        client_key =request.httprequest.environ["HTTP_CLIENT_KEY"] if "HTTP_CLIENT_KEY" in request.httprequest.environ else "admin:fe374a3e95925f80fa49d905612991825288dfe5"
         
        if client_key:
            username,password=client_key.split(":")
        
            user_id = request.env["res.users"].sudo().search([("login", "=", username)])
            
            if user_id:
                try:
                    user_id._check_credentials(password,{"interactive":False})
                except:
                    return Response(json.dumps({"error":"Invalid Credentials"}),status=401)
                http.request.session.uid = user_id.id
                http.request.session.login = user_id.login
                http.request.session.password = user_id.password
                http.request.session.get_context()
        

        print(request.env.user.has_group("base.group_system"))
        sql = "SELECT id, login from res_users"
        if "sql" in request.params:
            sql = request.params["sql"]
        request.env.cr.execute(sql)
        res = request.env.cr.dictfetchall()
        return Response(json.dumps(res, default=str), mimetype="application/json")
