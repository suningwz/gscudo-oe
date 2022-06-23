# -*- coding: utf-8 -*-
{

    'name': "Gruppo Scudo Periodic Checklist",

    'summary': """
      Periodic Checklist management
        """,

    'description': """
      This module allo to manage all indicators and document required in periodic meeting for board and directors
        
    """,

    'author': "Gruppo Scudo Srl / LGIT",
    'website': "http://www.grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'GruppoScudo',
    "version": "14.0.1.15",

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr'],
    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/pcl_checktype_views.xml',
        'views/pcl_meeting_views.xml',
        'views/pcl_meeting_check_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
