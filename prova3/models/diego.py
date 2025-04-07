
from odoo import models, fields

class Baubau(models.Model):
    _name = 'baubau'  # Nome del modello
    _description = 'Descrizione del modello Baubau'

    name = fields.Char(string='Nome', required=True)