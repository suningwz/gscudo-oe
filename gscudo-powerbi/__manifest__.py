# -*- coding: utf-8 -*-
{
    "name": "Gruppo Scudo PowerBI ",
    "summary": """
      Gruppo Scudo PowerBI Connector
        """,
    "description": """
      This module allow user get data for analize with PowerBI
        
    """,
    "author": "Gruppo Scudo Srl / LGIT",
    "website": "http://www.grupposcudo.it",
   
    "category": "GruppoScudo",
    "version": "14.0.1.20h",
    # any module necessary for this one to work correctly
    "depends": ["base", ],
    # always loaded
    "data": [
        #"security/ir.model.access.csv",
        # 'views/menus.xml',
        "views/views.xml",
        "views/templates.xml",
       
    ],
    # only loaded in demonstration mode
    "demo": [
        "demo/demo.xml",
    ],
}
