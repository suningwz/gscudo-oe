import datetime
from odoo import fields, models


class CallScheduler(models.TransientModel):
    _name = "call_scheduler"
    _description = "Wizard per lo scheduling delle chiamate"

    date_from = fields.Date(
        string="Da", default=fields.Date.context_today, required=True
    )
    date_to = fields.Date(string="A", default=fields.Date.context_today, required=True)
    call_per_day = fields.Integer(
        string="Chiamate al giorno", default=10, required=True
    )
    res_model_id = fields.Integer(
        default=lambda self: self.env["ir.model"]
        .search([("model", "=", "crm.lead")])
        .id
    )
    activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type", string="Tipo attività"
    )
    summary = fields.Char(string="Summary")

    #def _get_model_id(self):
        #return self.env["ir.model"].search([("model", "=", "crm.lead")])

    def schedule_call(self):
        # return all selected payments using active_ids
        # and you can filter them and use any validation you want
        leads = self.env["crm.lead"].browse(self._context.get("active_ids"))
        # loop the payments
        call_schedule = 0
        call_date = self.date_from
        for lead in leads:
            # lead.createcall(call_date)
            call_schedule += 1
            if call_schedule > self.call_per_day:
                call_date += datetime.timedelta(days=1)
                if call_date.weekday() >= 5:
                    call_date += datetime.timedelta(days=7 - call_date.weekday())
                if call_date > self.date_to:
                    break
                call_schedule = 0

            lead.message_subscribe(
                [lead.tmk_user_id.id or lead.user_id.id or self.env.user.id], None
            )
            activity_data = {
                "activity_type_id": 2,
                "res_model": "crm.lead",
                "res_model_id": self.env["ir.model"]
                .search([("model", "=", "crm.lead")])
                .id,
                "res_id": lead.id,
                "user_id": lead.tmk_user_id.id or lead.user_id.id or self.env.user.id,
                "date_deadline": call_date,
                "summary": self.summary,
                "activity_category": "default",
                "previous_activity_type_id": False,
                "recommended_activity_type_id": False,
            }

            self.env["mail.activity"].create(activity_data)
