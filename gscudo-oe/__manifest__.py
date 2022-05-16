{
    "name": "Gruppo Scudo Odoo Enterprise",
    "summary": """
        Gruppo Scudo Odoo Customizations
    """,
    "description": """
        This module customizes several Odoo models to fit GS needs.
    """,
    "license": "Other proprietary",
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "GruppoScudo",
    "version": "14.0.1.11",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
        "contacts",
        "project",
        "hr_timesheet",
        # 'helpdesk',
        "crm",
        "crm_lead_vat",
        "l10n_it_ateco",
    ],
    # always loaded
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        "security/custom_rules.xml",
        "data/ir_config_parameter.xml",
        "data/gs_partner_division.xml",
        "data/gs_product_family.xml",
        "views/gs_oe_menus.xml",
        "views/res_partner_views.xml",
        "views/hr_department_views.xml",
        "views/gs_product_family_views.xml",
        "views/project_project_views.xml",
        "views/crm_lead_views.xml",
        "views/crm_activity_report_views.xml",
        "views/call_scheduler_wizard.xml",
        "views/res_users_views.xml",
        "views/gs_worker_views.xml",
        "views/gs_worker_contract_views.xml",
        "views/gs_worker_job_type_views.xml",
        "views/gs_worker_job_views.xml",
        "views/product_template_views.xml",
    ],
}
