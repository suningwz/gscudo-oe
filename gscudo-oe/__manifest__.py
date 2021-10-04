# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo Odoo Enterprise",

    'summary': """
      Gruppo Scudo Odoo Customizations
        """,

    'description': """
      This module customize several Odoo models to fit GS needs
        
    """,

    'author': "Gruppo Scudo Srl / LGIT",
    'website': "http://www.grupposcudo.it",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.5',

    # any module necessary for this one to work correctly
    'depends': ['base', 
                #'contacts',
                'project',
                'hr_timesheet', 
                #'helpdesk', 
                'crm',
                'crm_lead_vat',	
                'l10n_it_ateco'],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/custom_rules.xml',
        'data/ir_config_parameter.xml',
        'data/gs_partner_division.xml',

        'views/res_partner_views.xml',
        'views/hr_department_views.xml',
        'views/project_project_views.xml',
        'views/crm_lead_views.xml',
        'views/crm_activity_report_views.xml',
        'views/call_scheduler_wizard.xml',
        'views/res_users_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
