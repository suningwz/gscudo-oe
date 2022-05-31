from odoo import fields, models


class GSLessonEnrollment(models.Model):
    _name = "gs_lesson_enrollment"
    _description = "Registrazione corso"

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
            # ("I", "identificato"),
            ("P", "proposto"),
            ("A", "accettato"),
            ("C", "confermato"),
        ],
        default="P",
    )
    active = fields.Boolean(string="Attivo", default=True)
    is_attendant = fields.Boolean(string="È presente", default=False)

    implicit = fields.Boolean(string="Iscrizione implicita", default=True)
    gs_course_enrollment_id = fields.Many2one(
        comodel_name="gs_course_enrollment", string="Iscrizione al corso"
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
