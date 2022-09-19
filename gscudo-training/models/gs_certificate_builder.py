from odoo import models, fields
from odoo.exceptions import UserError


class GSCertificateBuilder(models.Model):
    _name = "gs_certificate_builder"
    _description = "Creatore manuale certificati"
    _auto = False

    # FIXME mass update is_in_certificate

    name = fields.Char(string="Nome", compute="_compute_name")
    gs_worker_id = fields.Many2one(comodel_name="gs_worker", string="Lavoratore")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Azienda")
    gs_course_type_id = fields.Many2one(
        comodel_name="gs_course_type", string="Tipo di corso"
    )
    gs_lesson_enrollment_ids = fields.One2many(
        comodel_name="gs_lesson_enrollment",
        string="Lezioni seguite",
        compute="_compute_gs_lesson_enrollment_ids",
    )
    is_enough = fields.Boolean(string="Sufficiente")
    attended_hours = fields.Float(string="Ore totali")
    duration = fields.Float(string="Durata")
    attended_hours_display = fields.Char(
        "Ore seguite", compute="_compute_attended_hours_display"
    )
    last_lesson_date = fields.Date(string="Data ultima lezione")

    def _compute_name(self):
        for record in self:
            record.name = " - ".join(
                [record.gs_worker_id.name, record.gs_course_type_id.name]
            )

    def _compute_gs_lesson_enrollment_ids(self):
        for record in self:
            record.gs_lesson_enrollment_ids = self.env["gs_lesson_enrollment"].search(
                [
                    ("gs_worker_id", "=", record.gs_worker_id.id),
                    ("gs_course_type_id", "=", record.gs_course_type_id.id),
                    ("is_in_certificate", "=", False),
                ],
            )

    def _compute_attended_hours_display(self):
        def fft(t: float) -> str:
            hours = int(t)
            mins = int((t - hours) * 60)
            return f"{hours}:{mins:02}"

        for record in self:
            record.attended_hours_display = (
                fft(record.attended_hours) + "/" + fft(record.duration)
            )

    def generate(self):
        """Generate the certificate."""
        self.ensure_one()

        if not self.is_enough:
            raise UserError(
                "Le ore seguite non sono sufficienti per l'emissione del certificato"
            )

        previous_enrollment_id = False
        for enrollment in sorted(
            self.gs_lesson_enrollment_ids, key=lambda e: e.lesson_start_time
        ):
            enrollment.previous_enrollment_id = previous_enrollment_id
            previous_enrollment_id = enrollment

        new_cert_id = self.env["gs_worker_certificate"].create(
            {
                "gs_worker_id": self.gs_worker_id.id,
                "gs_training_certificate_type_id": (
                    self.gs_course_type_id.gs_training_certificate_type_id.id
                ),
                "is_update": self.gs_course_type_id.is_update,
                "type": "C",
                "issue_date": previous_enrollment_id.lesson_start_time.date(),
                "test_id": previous_enrollment_id.id,
                "attended_hours": self.attended_hours,
            }
        )
        for enrollment in self.gs_lesson_enrollment_ids:
            enrollment.is_in_certificate = True

        # FIXME go back to the tree
        return {
            "name": "Certificato generato",
            "type": "ir.actions.act_window",
            # "view_mode": "form",
            "res_model": "gs_worker_certificate",
            "res_id": new_cert_id.id,
            # "domain": [("id", "=", new_cert_id.id)],
            "target": "new",
        }

    def init(self):
        """At module install crate the view."""
        self._cr.execute(
            """
            drop view if exists gs_certificate_builder;
            create or replace view gs_certificate_builder as (
                select
                    row_number() over() as id,
                    w.id as gs_worker_id,
                    w.contract_partner_id as partner_id,
                    ct.id as gs_course_type_id,
                    case
                        when sum(le.attended_hours) > ct.duration * ct.min_attendance then true
                        else false
                    end as is_enough,
                    sum(le.attended_hours) as attended_hours,
                    ct.duration as duration,
                    -- ct.duration * ct.min_attendance as min_hours
                    case
                        when max(coalesce(l.start_time, '2099-12-31')) = '2099-12-31' then null
                        else max(l.start_time)
                    end as last_lesson_date
                from
                    gs_lesson_enrollment as le
                    left outer join gs_course as c on le.gs_course_id = c.id
                    left outer join gs_course_type as ct on c.gs_course_type_id = ct.id
                    inner join gs_worker as w on le.gs_worker_id = w.id
                    inner join gs_course_lesson as l on le.gs_course_lesson_id = l.id
                where
                    le.is_in_certificate = false
                    or le.is_in_certificate is null
                    and ct.mode != 'E'
                group by
                    w.id,
                    w.contract_partner_id,
                    ct.id
            )
            """
        )
