# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo Odoo Enterprise",

    'summary': """
        Common Configuration for Odoo 
        """,

    'description': """
      Common Configuration for Odoo 
        installet to have a bridge on sawgest 
        some personalizations on projects 
        
    """,

    'author': "Gruppo Scudo Srl",
    'website': "http://grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base','contacts'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv', 
        #'views/res_partner_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
