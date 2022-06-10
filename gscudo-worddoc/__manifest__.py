{
    "name": "Gruppo Scudo Mailmerge word document ",
    "summary": "Gruppo Scudo Mailmerge Word document",
    "description": (
      "This module allows to populate a custom defined template with fields "
      "and generate a word document or a pdf attachement."
    ),
    "author": "Gruppo Scudo Srl / LGIT",
    "license": "Other proprietary",
    "website": "http://www.grupposcudo.it",
    "category": "GruppoScudo",
    "version": "14.0.1.5",
    "depends": ["base", "mail"],
    # FIXME version?
    "external_dependencies": {"python": ["docxtpl"]},
    "data": [
        "security/ir.model.access.csv",
        "views/word_template_views.xml",
    ],
}
