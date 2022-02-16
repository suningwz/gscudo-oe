from odoo import api, fields, models


class GSPartnerEmployee(models.Model):
    _name = 'gs_worker'
    _description = 'Dipendente'

    name = fields.Char(string='Nominativo', compute="_compute_name",
                       inverse="_split_name", store=True)
    active = fields.Boolean(string='Attivo', default=True)
    birth_date = fields.Date(string='Data di nascita')
    birth_place = fields.Char(string='Luogo di nascita')
    birth_country = fields.Char(string='Stato di nascita')
    fiscalcode = fields.Char(string='Codice Fiscale')
    sex = fields.Selection(string='Sesso', selection=[(
        'M', 'Maschio'), ('F', 'Femmina'), ('X', 'X'), ])
    firstname = fields.Char(string='Nome', help='name', )
    surname = fields.Char(string='Cognome', help='surname', )
    working_hours = fields.Char(string='working_hours', help='working_hours', )
    use_videoterminals = fields.Boolean(
        string='use_videoterminals', help='use_videoterminals', )
    use_company_vehicles = fields.Boolean(
        string='use_company_vehicles', help='use_company_vehicles', )
    night_job = fields.Boolean(string='night_job', help='night_job', )
    work_at_height = fields.Boolean(
        string='work_at_height', help='work_at_height', )
    assumption_date = fields.Date(
        string='assumption_date', help='assumption_date', )
    phone_number = fields.Char(string='phone_number', help='phone_number', )
    email = fields.Char(string='email', help='email', )
    note  = fields.Char(string='Note')
    cartsan_id = fields.Char(string='ID CartSan')

    sg_worker_id = fields.Integer(string='ID SawGest')
    sg_updated_at  = fields.Datetime(string='Data Aggiornamento Sawgest')
    sg_synched_at = fields.Datetime(string='Data ultima Syncronizzazione sawgest')
    
    sg_url = fields.Char(string='Vedi in sawgest',
                         compute="_compute_sg_url", store=False)

    temp_partner_name = fields.Char(string='Azienda Temp')
    temp_sawgest_id = fields.Many2one(comodel_name='gs_clients', string='ID_SawGest', domain=[('deleted_at','=',False)])
    id_excel = fields.Char(string='ID Excel')
    
    def compute_worker_data(self):
        for record in self:
            
            partner_ids = self.env['gs_clients'].search(
                [('business_name', '=', record.temp_partner_name), ('deleted_at', '=', False)])
            if len(partner_ids) != 1:
                continue
                
            else:
                record.temp_sawgest_id = partner_ids[0]
                

    def _compute_sg_url(self):
        irconfigparam = self.env['ir.config_parameter']
        base_url = irconfigparam.sudo().get_param('sawgest_base_url')
        if base_url:
            for record in self:
                if record.sg_worker_id and record.sg_worker_id > 0:
                    record.sg_url = base_url + \
                        'workers/{}'.format(record.sg_worker_id)
                else:
                    record.sg_url = False

    @api.depends('firstname', 'surname')
    def _compute_name(self):
        for record in self:
            record.name = (record.surname or '') + \
                ' ' + (record.firstname or '')

    @api.depends('name')
    def _split_name(self):
        for record in self:
            splitted = str(record.name).split()
            if len(splitted) > 2:
                surname = splitted[0]
                splitted.pop(0)
                if len(surname) < 4:
                    surname = surname + ' ' + splitted[0]
                    splitted.pop(0)

                firstname = ' '.join(splitted)
            else:
                surname = splitted[0]
                firstname = splitted[1]

            record.surname = surname
            record.firstname = firstname

  
