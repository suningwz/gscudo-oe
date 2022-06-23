{
    "name": "Gruppo Scudo Word document composer",
    "summary": "Gruppo Scudo Word document composer",
    "description": (
        "This module allows to populate a custom defined template with fields "
        "and generate a word document."
    ),
    "author": "Gruppo Scudo Srl / LGIT",
    "license": "Other proprietary",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.15",
    "depends": ["base"],
    "external_dependencies": {"python": ["docxtpl"]},
    "data": [
        "security/ir.model.access.csv",
        "views/word_template_views.xml",
    ],
}
