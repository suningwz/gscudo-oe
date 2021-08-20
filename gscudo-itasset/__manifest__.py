# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo IT Assets",

    'summary': """
        Gestione ASSET IT """,

    'description': """
        ...
    """,

    'author': "Gruppo Scudo Srl / LGIT",
    'website': "http://www.grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',"web","gscudo-oe"],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/gs_itasset_views.xml',
        'views/hr_employee_views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
