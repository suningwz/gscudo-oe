from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def generate_training_planner_line(self):
        """Creates a new training planner line from the sale order."""
        planner_model = self.env["gs_training_planner"]

        for record in self:
            for line in record.order_line:
                planner_ids = planner_model.search(
                    [
                        ("sale_order_id", "=", record.id),
                        ("sale_order_line_id", "=", line.id),
                    ]
                )

                if planner_ids:
                    continue

                data = {
                    "sale_order_id": record.id,
                    "sale_order_line_id": line.id,
                    "partner_id": record.partner_id.id,
                }

                planner_model.create(data)

        return {
            "type": "ir.actions.act_window",
            "name": "Pianificatore Formazione",
            "res_model": "gs_training_planner",
            "views": [[False, "tree"], [False, "form"]],
            "target": "main",
            # 'domain' : [('id','in', new_ids)],
            "context": "{'search_default_created_today' : 1}",
        }
