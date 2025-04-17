from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LMSCategory(models.Model):
    _name = 'lms.category'
    _description = 'Learning Management System Category'
    _order = 'sequence, name asc'

    name = fields.Char(string='Category Name', required=True, translate=True)
    code = fields.Char(string='Code', copy=False, index=True)
    description = fields.Text(string='Description')  # Cambiato da 'note' a 'description' per coerenza
    image_1920 = fields.Image(string='Cover Image', max_width=1920, max_height=1920)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    topic_ids = fields.Many2many('lms.topic', string='Related Topics')
    tag_ids = fields.Many2many('slide.channel.tag', string='Tags')
    item_limit = fields.Integer(
        string='Item Limit', 
        default=10, 
        help="Maximum items allowed in this category (1-100)"
    )
    channel_ids = fields.Many2many(
        'slide.channel', 
        string='Courses',  # Modificato da 'Channels' a 'Courses' per chiarezza
        relation='lms_category_slide_channel_rel',
        column1='category_id',
        column2='channel_id'
    )
    website_id = fields.Many2one('website', string='Website')
    color = fields.Integer(string='Color Index')

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'Code must be unique per category!'),
    ]

    @api.constrains('item_limit')
    def _check_item_limit(self):
        for record in self:
            if not 1 <= record.item_limit <= 100:
                raise ValidationError(_('Item limit must be between 1 and 100!'))

    @api.model
    def create(self, vals):
        if not vals.get('code'):
            seq = self.env['ir.sequence'].next_by_code('lms.category.code') or '000'
            vals['code'] = f'CAT-{fields.Date.today().year}-{seq[-3:]}'
        return super().create(vals)

    def write(self, vals):
        # Aggiungi qui eventuali logiche di aggiornamento
        return super().write(vals)

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}" if record.code else record.name
            result.append((record.id, name))
        return result
    


class SlideChannel(models.Model):
    _inherit = 'slide.channel'
    
    category_ids = fields.Many2many(
        'lms.category',
        'slide_channel_category_rel',  # relation table name
        'channel_id',  # field for this model
        'category_id',  # field for related model
        string='Categories',
        help="Categories this channel belongs to"
    )