import base64
import logging
from tempfile import NamedTemporaryFile
import pytz
from odoo import http

logger = logging.getLogger(__name__)

try:
    from docxtpl import DocxTemplate
    from jinja2.exceptions import UndefinedError
except (ImportError, IOError) as err:
    logger.debug(err)
    raise


class SignatureSheetGenerator(http.Controller):
    @http.route(
        "/gscudo-training/doc/signature_sheet/<string:code>/<int:course_id>",
        auth="user",
    )
    def generate_signature_sheet(self, **kw):
        """
        Generates and returns the signature sheet.
        """
        try:
            template_code = kw["code"]
            course_id = kw["course_id"]
        except KeyError:
            return http.request.not_found()

        doc_template_ids = http.request.env["word_template"].search(
            [("code", "ilike", template_code)]
        )
        if not doc_template_ids:
            return http.request.not_found()
        doc_template = doc_template_ids[0]

        courses = http.request.env["gs_course"].search([("id", "=", course_id)])
        if not courses:
            return http.request.not_found()
        course = courses[0]

        # FIXME partner name
        def address(partner) -> str:
            return f"{partner.street} {partner.zip} {partner.city} ({partner.state_id.code})"

        def hours(time: int) -> str:
            hours = int(time)
            mins = int((time - hours) * 60)
            return f"{hours}:{mins:02}"

        user_tz = http.request.env.user.tz or "Europe/Rome"
        local = pytz.timezone(user_tz)

        # FIXME blocking requirements
        if any(l.start_time is False for l in course.gs_course_lesson_ids):
            return "Start time required for all lessons"

        data = {
            "protocol": course.protocol,
            "name": course.gs_course_type_id.name,
            "law_ref": course.gs_course_type_id.gs_training_certificate_type_id.law_ref,
            "duration": hours(course.duration),
            "content": course.gs_course_type_id.content,
            "lessons": [
                {
                    "location": address(l.location_partner_id),
                    "date": l.start_time.strftime("%d-%m-%Y"),
                    "start_time": l.start_time.astimezone(local).strftime("%H:%M"),
                    "end_time": l.end_time.astimezone(local).strftime("%H:%M"),
                    "teacher": l.teacher_partner_id.name,
                    "coteacher": (
                        l.coteacher_partner_id.name
                        if l.coteacher_partner_id.name is not False
                        else ""
                    ),
                    # FIXME order?
                    "workers": [
                        {
                            "name": e.gs_worker_id.name,
                            "fiscalcode": e.gs_worker_id.fiscalcode,
                            "job_description": (
                                e.gs_worker_id.contract_job_description
                                if e.gs_worker_id.contract_job_description is not False
                                else ""
                            ),
                            "partner": e.gs_worker_id.contract_partner_id.name,
                            "ateco": (
                                e.gs_worker_id.contract_partner_id.main_ateco_id.code
                                if e.gs_worker_id.contract_partner_id.main_ateco_id.code
                                is not False
                                else ""
                            ),
                        }
                        for e in l.gs_worker_ids
                        if e.state != "X"
                    ],
                }
                for l in sorted(course.gs_course_lesson_ids, key=lambda l: l.start_time)
                if not l.generate_certificate
            ],
        }

        # pylint: disable-next=consider-using-dict-items
        for key in data:
            # FIXME custom check tor lessons and workers
            if data[key] is False:
                return f"Missing data: {key}"

        # pylint: disable-next=consider-using-with
        f = NamedTemporaryFile()
        f.write(base64.b64decode(doc_template.template))
        document = DocxTemplate(f.name)

        try:
            document.render(data)
            document.save(f.name)
            return http.send_file(
                f, as_attachment=True, filename=f"Registro_{data['protocol']}.docx"
            )
        except UndefinedError as e:
            logger.error(
                "While generating template '%s' for object %s", template_code, course_id
            )
            logger.error(e)
            return "Error in the template"
