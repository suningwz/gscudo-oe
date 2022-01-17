# -*- coding: utf-8 -*-
{
    'name': "Gruppo Scudo Formazione ",

    'summary': """
      Gruppo Scudo Training Corse Management
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
    'version': '1.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'gscudo-oe'],

    # always loaded
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/gs_training_certificate_type_views.xml',
        'views/gs_course_type_views.xml',
        'views/gs_course_type_module_views.xml',
        'views/gs_course_views.xml',
        'views/gs_worker_job_type_views.xml',
        'views/gs_worker_job_views.xml',
        'views/gs_worker_views.xml',
        'views/gs_course_enrollment_views.xml',
        'views/gs_lesson_enrollment_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
