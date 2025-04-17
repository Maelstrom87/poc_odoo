from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LMSTopic(models.Model):
    _name = 'lms.topic'
    _description = 'Learning Management'