from odoo import api, fields, models


class GSPartnerEmployee(models.Model):
    _name = 'gs_employee'
    _description = 'Dipendente'

    name = fields.Char(string='Nominativo')
    birth_date = fields.Date(string='Data di nascita')
    fiscalcode = fields.Char(string='Codice Fiscale')
    sex = fields.Selection(string='Sesso', selection=[('X', 'X'), ('F', 'Femmina'),('M','Maschio')])
    name=fields.Char(string = 'name', help = 'name', )
    surname=fields.Char(string = 'surname', help = 'surname', )
    working_hours=fields.Char(string = 'working_hours', help = 'working_hours', )
    use_videoterminals=fields.Boolean(string = 'use_videoterminals', help = 'use_videoterminals', )
    use_company_vehicles=fields.Boolean(string = 'use_company_vehicles', help = 'use_company_vehicles', )
    dipendent=fields.Boolean(string = 'dipendent', help = 'dipendent', )
    night_job=fields.Boolean(string = 'night_job', help = 'night_job', )
    work_at_height=fields.Boolean(string = 'work_at_height', help = 'work_at_height', )
    assumption_date=fields.Date(string = 'assumption_date', help = 'assumption_date', )
    phone_number=fields.Char(string = 'phone_number', help = 'phone_number', )
    email=fields.Char(string = 'email', help = 'email', )
    
    
    
