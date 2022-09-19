{
    "name": "Gruppo Scudo Sorveglianza Sanitaria",
    "summary": """
        Il modulo gestisce i dati relativi alla sorveglianza sanitaria
    """,
    "description": """
      This module adds customizations to manage Training Courses
    """,
    "license": "Other proprietary",
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.20b",
    "depends": ["base", "gscudo-oe"],
    "data": [
        "data/gs_medical_check_frequency.csv",
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/menus.xml",
        "views/gs_medical_check_frequency_views.xml",
        "views/gs_medical_check_type_views.xml",
        "views/gs_worker_medical_check_views.xml",
        "views/gs_worker_views.xml",
        "views/inail_mod3b_views.xml",
        "views/inail_malprof_views.xml",
    ],
}
