from odoo import fields, models, api


class GSCourse(models.Model):
    _name = "gs_course"
    _description = "Corso"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    # TODO course name
    name = fields.Char(string="Corso")
    active = fields.Boolean(string="Attivo", default=True, tracking=True)

    protocol = fields.Char(string="Protocollo")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente")

    state = fields.Selection(
        [
            ("1-nuovo", "Da gestire"),
            ("2-proposto", "Proposto"),
            ("3-accettato", "Accettato"),
            ("4-in corso", "In corso"),
            ("5-concluso", "Concluso"),
        ],
        string="Stato",
        default="1-nuovo",
        tracking=True,
    )
    note = fields.Char(string="Note")
    max_workers = fields.Integer(string="Massimo iscritti", default=35, tracking=True)
    location_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Sede", tracking=True
    )
    start_date = fields.Date(string="Data inizio", tracking=True)
    end_date = fields.Date(string="Data termine", tracking=True)

    duration = fields.Float(
        string="Durata in ore", default=2, required=True, tracking=True
    )
    min_attendance = fields.Float(
        string="Partecipazione minima", required=True, default=0.9, tracking=True
    )

    gs_course_type_id = fields.Many2one(
        comodel_name="gs_course_type", string="Tipo Corso", tracking=True
    )
    mode = fields.Selection(
        string="Modalità",
        selection=[("P", "Presenza"), ("E", "E-learning"), ("M", "Misto")],
        default="P",
        tracking=True,
    )

    @api.onchange("gs_course_type_id")
    def _onchange_gs_course_type_id(self):
        self.mode = self.gs_course_type_id.mode
        self.duration = self.gs_course_type_id.duration
        self.min_attendance = self.gs_course_type_id.min_attendance

    is_multicompany = fields.Boolean(string="Multiazendale")

    parent_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso padre", tracking=True
    )
    children_course_ids = fields.One2many(
        comodel_name="gs_course",
        inverse_name="parent_course_id",
        string="Corsi figli",
    )

    is_child = fields.Boolean(
        string="Figlio",
        compute="_compute_is_child",
    )

    def _compute_is_child(self):
        for course in self:
            course.is_child = course.parent_course_id.id is not False

    total_enrolled = fields.Integer(
        string="Iscritti totali",
        compute="_compute_total_enrolled",
    )

    def _compute_total_enrolled(self):
        """
        This counts all the workers enrolled to at least one lesson of the course.
        """
        for course in self:
            enrolled = set([])
            for lesson in course.gs_course_lesson_ids:
                enrolled.update([e.gs_worker_id.id for e in lesson.gs_worker_ids])
            course.total_enrolled = len(enrolled)

    external_url = fields.Char(string="URL esterno")
