from odoo import fields, models

# TODO this is never used anywhere
class GSTrainingPlanner(models.Model):
    _name = "gs_training_planner"
    _description = "Planner Formazione"

    name = fields.Char(string="Name")
