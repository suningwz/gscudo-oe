import base64
from tempfile import NamedTemporaryFile
import zipfile

from odoo import http
from odoo.http import Response


class CertificateMassDownloader(http.Controller):
    @http.route(
        "/gscudo-training/doc/certificate/<string:ids>",
        auth="user",
    )
    def download_certificates(self, **kw):
        """
        Download the selected certificates.
        ids should be in the form id1,id2,id3,...,idn
        """
        try:
            ids_string: str = kw["ids"]
            ids = list(map(int, ids_string.split(",")))
        except (KeyError, ValueError):
            return Response("Richiesta malformata", status=400)

        model = http.request.env["gs_worker_certificate"]

        certs = model.search([("id", "in", ids)])

        f = NamedTemporaryFile("wb+")
        with zipfile.ZipFile(f, "w", zipfile.ZIP_DEFLATED) as archive:
            for cert in certs:
                if not cert.message_main_attachment_id:
                    return Response("Attestato mancante", status=400)
                archive.writestr(
                    cert.message_main_attachment_id.name.replace("/", ""),
                    base64.b64decode(cert.message_main_attachment_id.datas),
                )

        f.seek(0)
        return http.send_file(f, as_attachment=True, filename="certificati.zip")
