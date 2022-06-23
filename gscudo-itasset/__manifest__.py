{
    "name": "Gruppo Scudo IT Assets",
    "summary": """
        Gestione ASSET IT
    """,
    "description": """
        Il modulo consente di gestire gli asset it e la stampa delle credenziali di default
    """,
    "license": "Other proprietary",
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.15",
    "depends": ["base", "web", "hr"],
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "views/gs_itasset_menus.xml",
        "views/gs_itasset_views.xml",
        "views/gs_credential_views.xml",
        "views/hr_employee_views.xml",
        "reports/emp_itasset_template.xml",
        "reports/emp_itasset_report.xml",
        "reports/emp_credential_template.xml",
        "reports/emp_credential_report.xml",
    ],
}
