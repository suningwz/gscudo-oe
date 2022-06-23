import base64
import logging
from tempfile import NamedTemporaryFile
from odoo import http

logger = logging.getLogger(__name__)

try:
    from docxtpl import DocxTemplate
    from jinja2.exceptions import UndefinedError
except (ImportError, IOError) as err:
    logger.debug(err)
    raise


class Worddoc(http.Controller):
    @http.route("/gscudo-worddoc/doc/<string:code>/<int:obj_id>", auth="user")
    def render_doc(self, **kw):
        """
        Renders the template on an object and returns the file.
        """
        # verifica la presenza dei due parametri
        try:
            template_code = kw["code"]
            obj_id = kw["obj_id"]
        except KeyError:
            return http.request.not_found()

        doc_template_ids = http.request.env["word_template"].search(
            [("code", "ilike", template_code)]
        )
        if not doc_template_ids:
            return http.request.not_found()
        doc_template = doc_template_ids[0]

        obj_ids = http.request.env[doc_template.model.model].search(
            [("id", "=", obj_id)]
        )
        if not obj_ids:
            return http.request.not_found()
        obj = obj_ids[0]

        # in d the object is referred as "__s" for "self"
        d = dict(
            zip(
                ["__s"] + list(k for k in obj.fields_get()),
                [obj] + list(obj[v] for v in obj.fields_get()),
            )
        )

        if hasattr(obj, "word_doc_" + template_code):
            custom_method = getattr(obj, "word_doc_" + template_code)
            if callable(custom_method):
                d = custom_method()

        if "filename" in d:
            filename = d["filename"]
        else:
            filename = f"{template_code}_{obj_id}.docx"

        # with NamedTemporaryFile("w+b") as f:

        f = NamedTemporaryFile()
        f.write(base64.b64decode(doc_template.template))
        document = DocxTemplate(f.name)

        try:
            document.render(d)
            document.save(f.name)
            return http.send_file(f, as_attachment=True, filename=filename)
        except UndefinedError as e:
            logger.error(
                "While generating template '%s' for object %s", template_code, obj_id
            )
            logger.error(e)
            return "Error in the template"
