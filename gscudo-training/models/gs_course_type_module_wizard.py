from odoo import fields, models, api


class GSCourseTypeModuleWizard(models.TransientModel):
    _name = "gs_course_type_module_wizard"
    _description = "Wizard per la creazione di moduli formativi"

    name = fields.Char(string="Modulo")
    active = fields.Boolean(string="Attivo", default=True)
    content = fields.Text(string="Contenuto")

    note = fields.Char(string="Note")

    gs_course_type_id = fields.Many2one(
        comodel_name="gs_course_type",
        string="Corso",
        required=True,
    )

    sequence = fields.Integer(string="Sequenza", default=0)
    duration = fields.Float(string="Durata in ore")
    generate_certificate = fields.Boolean(string="Test finale", default=False)
    elearning = fields.Boolean(string="Modalità elearning")
    module_required_ids = fields.Many2many(
        comodel_name="gs_course_type_module",
        relation="gs_course_type_module_wizard_rel",
        column1="id",
        column2="alternate_id",
        string="Moduli Richiesti / Propedeutici",
    )

    remaining_hours = fields.Float(
        string="Ore rimanenti",
        compute="_compute_remaining_hours",
    )

    @api.depends("duration")
    def _compute_remaining_hours(self):
        """
        Compute the remaining hours for the selected course type.
        """
        for module in self:
            tot = module.gs_course_type_id.duration
            for mod in module.gs_course_type_id.gs_course_type_module_ids:
                tot -= mod.duration
            tot -= module.duration
            module.remaining_hours = tot

    def create_module(self):
        """
        Create the selected module.
        """
        self.ensure_one()
        self.env["gs_course_type_module"].create(
            {
                "name": self.name,
                "active": self.active,
                "content": self.content,
                "note": self.note,
                "gs_course_type_id": [(4, self.gs_course_type_id.id)],
                "sequence": self.sequence,
                "duration": self.duration,
                "generate_certificate": self.generate_certificate,
                "elearning": self.elearning,
                # "module_required_ids": [(6, 0, self.module_required_ids.ids)],
            }
        )
