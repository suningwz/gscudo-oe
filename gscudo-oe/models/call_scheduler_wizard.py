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
    res_model = fields.Char(string="Model", default = lambda self:self._context.get("active_model"))
    res_model_id = fields.Integer(string="res_model_id")
    user_id=fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    activity_type_id = fields.Many2one(
        comodel_name="mail.activity.type", string="Tipo attività"
    )

    activity_type_id_visible = fields.Boolean("Tipo attività visibile", default=True)
    user_id_visible = fields.Boolean("User_id visibile", default=True)

    summary = fields.Char(string="Summary")



    def schedule_call(self):
        """
        Schedule calls for the selected records.
        """
        active_model = self._context.get("active_model")
        res_model_id = self.env["ir.model"].search([("model", "=", active_model)])


        # get all selected records
        records = self.env[active_model].browse(self._context.get("active_ids"))

        call_schedule = 0
        call_date = self.date_from
        for record in records:
            # record.createcall(call_date)
            call_schedule += 1
            if call_schedule > self.call_per_day:
                call_date += datetime.timedelta(days=1)
                if call_date.weekday() >= 5:
                    call_date += datetime.timedelta(days=7 - call_date.weekday())
                if call_date > self.date_to:
                    break
                call_schedule = 0

            # record.message_subscribe(
            #     [record.tmk_user_id.id or record.user_id.id or self.env.user.id], None
            # )

            ### Identifica lo User_id
            ### se è un lead usa il tmk altrimente cerca il tmk associato al partner o all'oggetto


            activity_data = {
                "activity_type_id": record.activity_type_id or 2,
                "res_model": active_model,
                "res_model_id": res_model_id.id,
                "res_id": record.id,
                "user_id": record.user_id.id or record.tmk_user_id.id or self.env.user.id,
                "date_deadline": call_date,
                "summary": self.summary,
                "activity_category": "default",
                "previous_activity_type_id": False,
                "recommended_activity_type_id": False,
            }

            self.env["mail.activity"].create(activity_data)
