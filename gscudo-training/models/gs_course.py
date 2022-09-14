import random
from odoo import fields, models, api
from odoo.exceptions import UserError


class GSCourse(models.Model):
    _name = "gs_course"
    _description = "Corso"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    def _get_document_folder(self):
        return self.env["documents.folder"].search([("name", "=", "Formazione")])

    def _get_document_tags(self):
        # pylint: disable-next=no-else-return
        if self.generate_certificate:
            return self.env["documents.tag"].search([("name", "=", "Test finale")])
        else:
            return self.env["documents.tag"].search([("name", "=", "Foglio firme")])

    name = fields.Char(string="Corso", index=True, compute="_compute_name", store=True)

    @api.depends("gs_course_type_id", "protocol", "start_date")
    def _compute_name(self):
        for course in self:
            course.name = " - ".join(
                [
                    course.gs_course_type_id.name or "",
                    course.protocol or "",
                    course.start_date.strftime("%d/%m/%Y")
                    if course.start_date
                    else "data da definire",
                ]
            )

    active = fields.Boolean(string="Attivo", default=True, tracking=True)

    protocol = fields.Char(string="Protocollo", index=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string="Cliente")

    state = fields.Selection(
        [
            ("1-nuovo", "Da gestire"),
            ("2-proposto", "Proposto"),
            ("3-accettato", "Accettato"),
            ("4-in corso", "In corso"),
            ("5-concluso", "Concluso"),
            ("X-annullato", "Annullato"),
        ],
        string="Stato",
        default="1-nuovo",
        tracking=True,
        group_expand="_group_expand_states",
    )

    def _group_expand_states(self, _states, _domain, _order):
        return [key for key, _ in type(self).state.selection]

    note = fields.Char(string="Note")
    max_workers = fields.Integer(string="Massimo iscritti", default=35, tracking=True)
    location_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Sede", tracking=True
    )

    teacher_partner_id = fields.Many2one(
        comodel_name="res.partner", string="Docente", tracking=True
    )

    start_date = fields.Date(string="Data inizio", tracking=True, index=True)
    end_date = fields.Date(string="Data termine", tracking=True, index=True)

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
        self._compute_name()
        self.mode = self.gs_course_type_id.mode
        self.duration = self.gs_course_type_id.duration
        self.min_attendance = self.gs_course_type_id.min_attendance
        self.max_workers = self.gs_course_type_id.max_workers
        self.is_internal = self.gs_course_type_id.is_internal
        self.document_template_id = self.gs_course_type_id.document_template_id

    @api.onchange("start_date")
    def _onchange_start_date(self):
        self._compute_name()

    is_multicompany = fields.Boolean(string="Multiazendale")

    is_internal = fields.Boolean(
        string="Corso gestito",
        help=(
            "Decide se l'attestato è generato da Odoo o importato esternamente. "
            "Esempi di corsi non interni sono i corsi AiFOS e quelli organizzati da "
            "Officina del Carrello."
        ),
        default=True,
    )

    document_template_id = fields.Many2one(
        comodel_name="word_template",
        string="Modello attestato",
        default=lambda self: (
            self.env["word_template"].search(
                [("code", "ilike", "default_certificate_template")],
                limit=1,
            )
            or False
        ),
        domain=[("model.model", "=", "gs_worker_certificate")],
    )

    parent_course_id = fields.Many2one(
        comodel_name="gs_course", string="Corso padre", tracking=True
    )
    children_course_ids = fields.One2many(
        comodel_name="gs_course",
        inverse_name="parent_course_id",
        string="Corsi figli",
    )

    @api.onchange("parent_course_id")
    def _onchange_parent_course_id(self):
        if self.parent_course_id:
            self.partner_id = self.parent_course_id.partner_id
            self.state = self.parent_course_id.state
            self.start_date = self.parent_course_id.start_date
            self.end_date = self.parent_course_id.end_date
            self.duration = self.parent_course_id.duration

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
                enrolled.update(
                    [
                        e.gs_worker_id.id
                        for e in lesson.gs_worker_ids
                        if e.state not in ["X", "I", "P"]
                    ]
                )
            course.total_enrolled = len(enrolled)

    external_url = fields.Char(
        string="URL esterno", compute="_compute_external_url", store=True
    )
    published = fields.Boolean(string="Pubblicato sul sito", default=False)

    id_sawgest = fields.Integer(string="Id Sawgest", index=True)

    @api.depends("id_sawgest")
    def _compute_external_url(self):
        for course in self:
            if (
                course.id_sawgest is not False
                and course.id_sawgest > 0
                and course.external_url is False
            ):
                course.external_url = (
                    "https://gestionale.grupposcudo.it/#/app/training_timetables/"
                    f"training_class_course/{course.id_sawgest}/1/1/"
                )

    @api.model
    def create(self, vals):
        """
        On course creation, generate an automatic protocol number if it is not
        manually assigned.
        """
        course = super().create(vals)

        if vals.get("protocol", False) is False:
            course.protocol = f"COUR-{course.id}"
            self._compute_name()

        return course

    def enrollment_wizard(self):
        """
        Given one or more training needs, call the enrollment wizard
        on the selected worker(s) for courses of the right type.
        """
        if not self:
            raise UserError("Nessun corso selezionato")

        if len(self) > 1:
            raise UserError("Azione disponibile per un corso alla volta")

        cert_type_id = self.gs_course_type_id.gs_training_certificate_type_id

        action = {
            "name": "Iscrivi lavoratore",
            "view_mode": "form",
            "type": "ir.actions.act_window",
            "target": "new",
            "res_model": "gs_course_enrollment_wizard",
            "context": {
                "default_gs_training_certificate_type_id": cert_type_id.id,
                "active_id": self.env.context.get("active_id"),
            },
        }

        return action

    @staticmethod
    def rand():
        """
        Return a random 6 character string.
        """
        return str(random.randint(100000, 999999))

    def participants_mail(self):
        self.ensure_one()

        mail = []
        missing = []
        for enrollment in self.gs_worker_ids:
            worker = enrollment.gs_worker_id
            if worker.email:
                mail.append(worker.email)
            else:
                missing.append(worker.name)

        message = ""  # f"<p>Mail presenti:<br/><pre>{'\n'.join(mail)}</pre></p>"
        if missing:
            # FIXME finish this
            message += ""  # f"<p>Mail mancanti:<ul/>{'\n'.join(mail)}</ul></p>"

        return self.env["gs_message_wizard"].create({"message": message})
