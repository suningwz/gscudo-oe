from odoo import fields, models, api


class GSLessonEnrollment(models.Model):
    _name = "gs_lesson_enrollment"
    _description = "Registrazione corso"

    # FIXME lesson enrollment name
    name = fields.Char(string="Nome")
    gs_course_lesson_id = fields.Many2one(
        comodel_name="gs_course_lesson", string="Lezione"
    )
    gs_course_id = fields.Many2one(
        comodel_name="gs_course",
        string="Corso",
        related="gs_course_lesson_id.gs_course_id",
        store=True,
    )

    gs_worker_id = fields.Many2one(comodel_name="gs_worker", string="Lavoratore")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Azienda",
        related="gs_worker_id.contract_partner_id",
    )

    state = fields.Selection(
        string="Stato",
        selection=[
            # ("I", "Identificato"),
            ("P", "Proposto"),
            ("A", "Accettato"),
            ("C", "Confermato"),
        ],
        default="P",
    )
    active = fields.Boolean(string="Attivo", default=True)
    is_attendant = fields.Boolean(string="È presente", default=False)
    attended_hours = fields.Float(
        string="Ore frequentate",
        default=0.0,
    )

    @api.onchange("is_attendant")
    def _onchange_is_attendant(self):
        """
        By default, workers attend the whole lesson.
        """
        if self.gs_course_lesson_id.gs_course_type_module_id.generate_certificate:
            return

        if self.is_attendant:
            self.attended_hours = self.gs_course_lesson_id.duration
        else:
            self.attended_hours = 0.0

    implicit = fields.Boolean(string="Iscrizione implicita", default=True)
    gs_course_enrollment_id = fields.Many2one(
        comodel_name="gs_course_enrollment", string="Iscrizione al corso"
    )

    def generate_certificate(self):
        """
        Generate certificates for the workers that passed the final test.
        """
        # logging.warning(self.env.context.get("active_ids"))
        # for test in self.env.context.get("active_ids"):
        for test in self:
            if not test.is_attendant:
                # The worker did not pass the final test
                # UserError("Il lavoratore non ha superato il test finale.")
                continue

            certificate_type_id = (
                # fmt: off
                test
                .gs_course_id
                .gs_course_type_id
                .gs_training_certificate_type_id
                .id
                # fmt: on
            )

            if self.env["gs_worker_certificate"].search(
                [
                    ("gs_worker_id", "=", test.gs_worker_id.id),
                    ("gs_training_certificate_type_id", "=", certificate_type_id),
                    ("issue_date", "=", test.gs_course_id.end_date),
                ]
            ):
                # Certificate already generated
                continue

            if test.is_attendant:
                self.env["gs_worker_certificate"].create(
                    {
                        "gs_worker_id": test.gs_worker_id.id,
                        "gs_training_certificate_type_id": certificate_type_id,
                        "type": "C",
                        "issue_date": test.gs_course_id.end_date,
                    }
                )


class GSCourseLesson(models.Model):
    _inherit = "gs_course_lesson"

    gs_worker_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        inverse_name="gs_course_lesson_id",
        string="Iscritti",
    )


class GSCourseEnrollment(models.Model):
    _inherit = "gs_course_enrollment"

    gs_lesson_enrollment_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        inverse_name="gs_course_enrollment_id",
        string="Iscrizione Lezioni",
    )


class GSWorker(models.Model):
    _inherit = "gs_worker"

    gs_lesson_enrollment_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        inverse_name="gs_worker_id",
        string="Lezioni",
        groups="gscudo-training.group_training_backoffice",
    )
