#-*- coding: utf-8 -*-
import json
from odoo import http
from odoo.tools import date_utils

class GscudoConnector(http.Controller):
    
    @http.route('/connector/some_html', type="http", auth='public')
    def some_html(self):
        """return sample text"""
        return "<h1>This is a test</h1>"

    @http.route('/connector/some_json', type="json", auth='public')
    def some_json(self):
        """ Return sample json """
        return {"sample_dictionary": "This is a sample JSON dictionary"}   

    @http.route('/connector/mydata', type="http", auth='public')
    def mydata(self):
        """ Return sample data """
        company = http.request.env['res.partner'].sudo().search([],limit=10)
        raw_data = company.read(['name', 'street', 'city', 'country_id'])
        json_data = json.dumps(raw_data, default=date_utils.json_default)
        str(json_data).replace("[","").replace("]","")
        return json_data   
