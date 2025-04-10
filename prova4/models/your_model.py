# models/your_model.py
from odoo import models, fields

class YourModel(models.Model):
    _name = "your.model.name"
    _description = "Your Model Description"

    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")