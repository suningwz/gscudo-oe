from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def generate_medical_planner_line(self):
        """Creates a new medical planner line from the sale order."""
        planner_model = self.env["gs_medical_planner"]

        new_lines = []

        for record in self:
            planner_ids = planner_model.search([("sale_order_id", "=", record.id)])

            if planner_ids:
                new_lines.extend([p.id for p in planner_ids])
                continue

            data = {
                "sale_order_id": record.id,
                "partner_id": record.partner_id.id,
            }

            new_line = planner_model.create(data)
            new_lines.append(new_line)

        return {
            "type": "ir.actions.act_window",
            "name": "Pianificatore sorveglianza sanitaria",
            "res_model": "gs_medical_planner",
            "views": [[False, "tree"], [False, "form"]],
            "target": "main",
            "domain": [("id", "in", new_lines)],
        }
