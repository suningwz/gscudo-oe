{
    "name": "Gruppo Scudo Formazione ",
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
    "version": "14.0.1.10",
    "depends": ["base", "sale", "gscudo-oe"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/gs_training_menus.xml",
        "views/gs_certificate_type_views.xml",
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
    ],
}
