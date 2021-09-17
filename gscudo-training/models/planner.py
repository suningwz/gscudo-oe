from odoo import _, api, fields, models


class Planner(models.Model):
    _name = 'gstraining_planner'
    _description = 'Pianificatore'

    name = fields.Char(string='Corso')
    course_date = fields.Date(string='Data')
    lesson_dates= fields.Char(string='Date corso')
    lesson_times = fields.Char(string='Orario')
    course_type = fields.Selection(string='', selection=[('M', 'Multiaziendale'), ('X', 'X')])
    
    partner_id = fields.Many2one(comodel_name='res.partner', string='Cliente')
    place = fields.Char(string='Luogo')
    offer_id = fields.Char(string='N. Offerta')
    offer_date = fields.Date(string='Data offerta')
    unit_price = fields.Float(string='Imponibile',help="Imponibile a persona o a corso" )
    total_price = fields.Float(string='Totale',help="Imponibile totale" )
    customer_order = fields.Char(string='Ordine Cliente')
    customer_payment = fields.Char(string='Metodo Pagamento')
    
    

    course_family = fields.Char(string='Famiglia')

    tot_hours = fields.Float(string='Nr. Ore', )
    tot_qty = fields.Integer(string='Q.tà')
    tutor  = fields.Char(string='Fornitore')
    tutor_price = fields.Float(string='Prezzo fornitore')
    tutor_order_GS = fields.Char(string='Ordine GS')
    
    place_supplier = fields.Char(string='Fornitore Sala')
    place_price = fields.Float(string='Prezzo Sala')
    material_supplier = fields.Char(string='Fornitore Materali')
    material_price = fields.Float(string='Prezzo Materiali')
    note = fields.Text(string='Note')
    
    
    
    
    
    
    ####Dati mancanti
    # DATA COMPLETA 
    # FATTURADATA OFFERTA	 IMPONIBILE a persona o a corso[EURO] 	 IMPONIBILE TOTALE 	FAMIGLIA	NR. ORE	QUANTITA'	ORARIO	PARTECIPANTI	TIPO CORSO CLIENTE O MULTIAZIENDALE	FORNITORE	 COSTO FORNITORE 	FORNITORE SALA	 COSTO FORNITORE SALA 	FORNITORE MATERIALE	COSTO FORNITORE MATERIALE	NR. ORDINE GS MATERIALE	CORSISTA PER RECUPERO	NR. ORDINE CLIENTE	NR. ORDINE GS	DATA ORDINE GS	METODO DI PAGAMENTO	NOTE
