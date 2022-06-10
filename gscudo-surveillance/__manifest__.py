# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo Sorveglianza Sanitaria",

    'summary': """
        Il modulo gestisce i dati relativi alla sorveglianza sanitaria """,

    'summary': """
      Gruppo Scudo Health Surveillance  Management
        """,

    'description': """
      This module adds customizations to manage Training Courses
        
    """,

    'author': "Gruppo Scudo Srl / LGIT",
    'website': "http://www.grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'GruppoScudo',
     "version": "14.0.1.15",

    # any module necessary for this one to work correctly
    'depends': ['base', 'gscudo-oe'],


    # always loaded
    'data': [
        'data/gs_medical_check_frequency.csv',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/gs_medical_check_frequency_views.xml',
        'views/gs_medical_check_type_views.xml',
        'views/gs_worker_medical_check_views.xml',
        'views/gs_worker_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
