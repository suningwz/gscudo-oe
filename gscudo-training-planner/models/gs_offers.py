from datetime import datetime

from odoo import models


class GsOffers(models.Model):
    _inherit = "gs_offers"

    def generate_training_planner(self):
        _new_ids = []
        creation_date = datetime.now()
        for record in self:
            for article in record.article_ids:
                planner_ids = self.env["gstraining_planner"].search(
                    [
                        ("gs_offer_id", "=", record.id),
                        ("gs_article_id", "=", article.id),
                    ]
                )
                if len(planner_ids) > 0:
                    continue
                data = {
                    "gs_offer_id": record.id,
                    "gs_article_id": article.id,
                    "gs_client_id": record.client_id.id,
                    "creation_date": creation_date,
                }
                # planner= self.env["gstraining_planner"].create(data)
                _new_ids.append(self.env["gstraining_planner"].create(data).id)
                # planner._compute_article_price()

        return {
            "type": "ir.actions.act_window",
            "name": "Pianificatore Formazione",
            "res_model": "gstraining_planner",
            "views": [[False, "tree"], [False, "form"]],
            "target": "main",
            # 'domain' : [('id','in', new_ids)],
            "context": "{'search_default_created_today' : 1}",
        }
