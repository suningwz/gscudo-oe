# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo Portal ",

    'summary': """
      Gruppo Scudo Portal Management
        """,

    'description': """
      This module allow customer portal access to manage various operations
        
    """,

    'author': "Gruppo Scudo Srl / LGIT",
    'website': "http://www.grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'GruppoScudo',
     "version": "14.0.1.15",
    # any module necessary for this one to work correctly
    'depends': ['base', 'gscudo-oe', 'gscudo-training'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/portal_security.xml',
        # 'views/menus.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/portal_worker_template.xml',
        'views/portal_gs_worker_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
