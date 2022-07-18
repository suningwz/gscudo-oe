from odoo import fields, models


class GSCourseTypeModule(models.Model):
    _name = "gs_course_type_module"
    _description = "Modulo"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Modulo", tracking=True)
    active = fields.Boolean(string="Attivo", default=True, tracking=True)
    content = fields.Text(string="Contenuto", tracking=True)

    note = fields.Char(string="Note", tracking=True)

    gs_course_type_id = fields.Many2many(
        comodel_name="gs_course_type",
        relation="gs_course_type_module_course_type_rel",
        column1="gs_course_type_module_id",
        column2="gs_course_type_id",
        string="Corsi associati",
        tracking=True,
    )
    sequence = fields.Integer(string="Sequenza", default=0)
    duration = fields.Float(string="Durata in ore", tracking=True)
    generate_certificate = fields.Boolean(
        string="Test finale", default=False, tracking=True
    )
    elearning = fields.Boolean(string="Modalità elearning", tracking=True)
    module_required_ids = fields.Many2many(
        comodel_name="gs_course_type_module",
        relation="gs_course_type_module_rel",
        column1="id",
        column2="alternate_id",
        string="Moduli Richiesti / Propedeutici",
    )


class GSCourseType(models.Model):
    _inherit = "gs_course_type"
    gs_course_type_module_ids = fields.Many2many(
        comodel_name="gs_course_type_module",
        relation="gs_course_type_module_course_type_rel",
        column1="gs_course_type_id",
        column2="gs_course_type_module_id",
        string="Moduli",
        tracking=True,
    )
