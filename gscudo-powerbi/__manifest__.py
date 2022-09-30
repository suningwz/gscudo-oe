# -*- coding: utf-8 -*-
{
    "name": "Gruppo Scudo PowerBI ",
    "summary": """
      Gruppo Scudo PowerBI Connector
        """,
    "description": """
      This module allow user get data for analize with PowerBI

      Usage:

      - every user must create an own api key in the user form
      - PowerBi manager can ceate a single query 
      - Each query can be associated to some groups, if no groups query will be available for all users
      - In query  you can use uid parameter to filter data for specific user (eg: select * from res_users where id = %(uid)s ; )
      -
        
    """,
    "author": "Gruppo Scudo Srl / LGIT",
    "license": "Other proprietary",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.23b",
    # any module necessary for this one to work correctly
    "depends": [
        "base",
    ],
    # always loaded
    "data": [
        "security/security_groups.xml",
        "security/ir.model.access.csv",
        # 'views/menus.xml',
        "views/views.xml",
        "views/templates.xml",
        "views/gs_powerbi_query_views.xml",
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
