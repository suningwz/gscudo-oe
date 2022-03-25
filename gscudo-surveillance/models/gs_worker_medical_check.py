from odoo import api, fields, models


class WorkerMedicalCheck(models.Model):
    _name = 'gs_worker_medical_check'
    _description = 'Esami / Visite'

    name = fields.Char(string='Descrizione visita')
    active = fields.Boolean(string='Attivo', default = True)
    gs_worker_id = fields.Many2one(comodel_name='gs_worker', string='Lavoratore')
    contract_partner_id = fields.Many2one(related='gs_worker_id.contract_partner_id', string='Azienda')
    doctor = fields.Char(related='contract_partner_id.doctor', string='Medico competente')
    medical_locum = fields.Char(string='Medico sostituto')
    
    fiscalcode = fields.Char(related='gs_worker_id.fiscalcode', string='Codice Fiscale')
    email = fields.Char(related='gs_worker_id.email', string='Email')
    birth_date = fields.Date(related='gs_worker_id.birth_date', string='Data di nascita')
    birth_place = fields.Char(related='gs_worker_id.birth_place', string='Luogo di nascita')
    execution_date = fields.Date(string='Data Esecuzione')
    gs_medical_check_type_id = fields.Many2one(comodel_name='gs_medical_check_type', string='Visita / Esame')
    expiry_date = fields.Date(string='Data Scadenza')
    schedule_time = fields.Datetime(string='Data ora prenotazione')
    gs_medical_check_frequency_id = fields.Many2one(comodel_name='gs_medical_check_frequency', string='Frequenza')
    note = fields.Text(string='Note')


class GSWorker(models.Model):
    _inherit = 'gs_worker'

    gs_worker_medical_check_ids = fields.One2many(comodel_name='gs_worker_medical_check', inverse_name='gs_worker_id', string='Visite/ Analisi')
    
    
    