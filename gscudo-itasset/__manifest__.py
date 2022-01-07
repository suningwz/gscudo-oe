# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo IT Assets",

    'summary': """
        Gestione ASSET IT """,

    'description': """
        Il modulo consente di gestire gli asset it e la stampa delle credenziali di default
    """,

    'author': "Gruppo Scudo Srl / LGIT",
    'website': "http://www.grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'GruppoScudo',
    'version': '1.3',

    # any module necessary for this one to work correctly
    'depends': ['base',"web","hr"],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/gs_itasset_views.xml',
        'views/gs_credential_views.xml',
        'views/hr_employee_views.xml',
        'reports/emp_itasset_template.xml',
        'reports/emp_itasset_report.xml',
        'reports/emp_credential_template.xml',
        'reports/emp_credential_report.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
