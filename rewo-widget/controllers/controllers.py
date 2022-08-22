# -*- coding: utf-8 -*-
from odoo import http
from odoo import api, fields, models

from  http import client as http_client 
import base64

class RewoWidget(http.Controller):

    @http.route('/rewo-widget/dial/<num2dial>', auth='user')
    def dial(self, num2dial):
        irconfigparam = http.request.env["ir.config_parameter"]
        server=irconfigparam.sudo().get_param("rewo_api_server")
        url=irconfigparam.sudo().get_param("rewo_api_url")
        username = http.request.env.user.email
        password = http.request.env.user.rewo_password
        conn = http_client.HTTPSConnection(server, timeout = 1000)
            
        payload = ''
        headers = {
        'Authorization': 'Basic {}'.format(base64.b64encode(bytes("{}:{}".format(username,password),'utf-8')).decode('ascii')),
        }
        conn.request("POST", "{}user/{}/calls/new?address={}".format(url,username,num2dial), payload, headers)
        res = conn.getresponse()
        data = res.read()
        
        return (data.decode("utf-8"))

    
