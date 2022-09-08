{
    "name": "Gruppo Scudo Formazione",
    "summary": """
        Gruppo Scudo Training Course Management
    """,
    "description": """
        This module adds customizations to manage Training Courses.
    """,
    "license": "Other proprietary",
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.21a",
    "depends": ["base", "sale", "gscudo-oe", "documents", "gscudo-worddoc"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "data/signature_sheet_action.xml",
        "views/gs_course_type_module_wizard_views.xml",
        "views/gs_course_enrollment_wizard_views.xml",
        "views/gs_lesson_enrollment_wizard_views.xml",
        "views/gs_training_need_wizard_views.xml",
        "views/gs_training_menus.xml",
        "views/gs_training_certificate_type_views.xml",
        "views/gs_course_lesson_views.xml",
        "views/gs_course_type_views.xml",
        "views/gs_course_type_module_views.xml",
        "views/gs_course_views.xml",
        "views/gs_worker_job_type_views.xml",
        "views/gs_worker_job_views.xml",
        "views/gs_worker_views.xml",
        "views/gs_course_enrollment_views.xml",
        "views/gs_lesson_enrollment_views.xml",
        "views/gs_worker_certificate_views.xml",
        "views/product_template_views.xml",
        "views/res_partner_views.xml",
        "automation/automatic_actions.xml",
    ],
}
