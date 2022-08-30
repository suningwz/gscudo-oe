# -*- coding: utf-8 -*-
{
    "name": "Gruppo Scudo Rewo Widget",
    "summary": """
        Gruppo Scudo Odoo Widget for Rewo Dial in
    """,
    "description": """
        This module allow user to dial directly on rewo PABX 
    """,
    "license": "Other proprietary",
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.21",
    "depends": [
        "base",
        "contacts",
    ],
    "qweb": [
        "static/src/xml/qweb_template.xml",
    ],
    # always loaded
    "data": [
        # 'security/ir.model.access.csv',
        "data/ir_config_parameter.xml",
        "views/views.xml",
        "views/templates.xml",
    ],
}
