{
    "name": "Gruppo Scudo Pianificatore Formazione",
    "summary": """
        Gruppo Scudo Training Course additional management
    """,
    "description": """
        This module adds customizations to manage Training Courses
    """,
    "license": "Other proprietary",
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.23",
    "depends": [
        "base",
        "contacts",
        "project",
        "gscudo-oe",
        "gscudo-training",
    ],
    "data": [
        "security/ir.model.access.csv",
        "security/security_groups.xml",
        "views/menus.xml",
        "views/planner_views.xml",
        "views/gs_course_enrollment_views.xml",
        "views/gs_course_views.xml",
        "views/gs_enrollment_wizard_views.xml",
        "data/sale_order_actions.xml",
        "data/mail_template.xml",
    ],
    "demo": [],
}
