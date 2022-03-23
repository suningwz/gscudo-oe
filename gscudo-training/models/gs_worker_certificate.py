from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

import datetime
from datetime import timezone, datetime, timedelta, date
from dateutil.relativedelta import relativedelta

class WorkerCertificate(models.Model):
    _name = 'gs_worker_certificate'
    _description = 'Certificazioni'

    name = fields.Char(string='Certificazione')
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore', index=True)
    contract_partner_id = fields.Many2one(related="gs_worker_id.contract_partner_id", comodel_name='res.partner', string='Azienda/Sede', store=True, index=True)

    gs_training_certificate_type_id = fields.Many2one(comodel_name='gs_training_certificate_type', string='Tipo certificazione', )
    type = fields.Selection(string='Tipo', selection=[('C', 'Certificato'), ('E', 'Esigenza formativa'),], default='E')
    active = fields.Boolean(string='Attivo', default = True)
    
    issue_date = fields.Date(string='Data attestato')
    issue_serial = fields.Char(string='Protocollo attestato')
  
    expiry_date = fields.Date(string='Data scadenza', index=True)

    @api.constrains('issue_date', 'expiry_date')
    def _check_date(self):
        if self.expiry_date != False:
            if self.expiry_date != False :
                if self.issue_date > self.expiry_date:
                    raise ValidationError(
                        'La data di scadenza  deve essere maggiore di quella dell\' attestato')
                



    note = fields.Char(string='Note')

    expired = fields.Boolean(string='Scaduto', compute='_compute_expiration', )
    expiring = fields.Boolean(string='In scadenza', compute='_compute_expiration', )

    @api.onchange('issue_date','gs_training_certificate_type_id')
    def _compute_expiry_date(self):
        for record in self:
            if record.issue_date != False and record.gs_training_certificate_type_id != False:
                record.expiry_date = record.issue_date + relativedelta(years=record.gs_training_certificate_type_id.update_interval)

    @api.depends('expiry_date')
    def _compute_expiration(self):
        for record in self:
            record.expired=False
            record.expiring = False
            if record.expiry_date != False:
                if record.expiry_date < datetime.now().date():
                    record.expired=True
                    record.expiring = False
                elif record.expiry_date < datetime.now().date()+ relativedelta(months=2):
                    record.expired=False
                    record.expiring = True
    sg_id = fields.Integer(string='ID SawGest')
    sg_updated_at  = fields.Datetime(string='Data Aggiornamento Sawgest')
    sg_synched_at = fields.Datetime(string='Data ultima Syncronizzazione sawgest')
    
    sg_url = fields.Char(string='Vedi in sawgest',
                         compute="_compute_sg_url", store=False)

    def _compute_sg_url(self):
        irconfigparam = self.env['ir.config_parameter']
        base_url = irconfigparam.sudo().get_param('sawgest_base_url')
        if base_url:
            for record in self:
                if record.sg_id and record.sg_id > 0:
                    record.sg_url = base_url + \
                        'training_timetables/{}'.format(record.sg_id)
                else:
                    record.sg_url = False
            

class Worker(models.Model):
    _inherit = 'gs_worker'

    gs_worker_certificate_ids = fields.One2many(comodel_name='gs_worker_certificate', inverse_name='gs_worker_id', string='Attestati',
        groups="gscudo-training.group_training_backoffice")

    
    
    
