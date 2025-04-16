from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class LMSCategory(models.Model):
    _name = 'lms.category'
    _description = 'Learning Management System Category'
    _order = 'sequence, name asc'

    name = fields.Char(string='Category Name', required=True, translate=True)
    code = fields.Char(string='Code', copy=False, index=True)
    note = fields.Text(string='Description')
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    topic_ids = fields.Many2many('lms.topic', string='Related Topics')
    tag_ids = fields.Many2many('slide.channel.tag', string='Tags')
    item_limit = fields.Integer(string='Item Limit', default=10, help="Maximum items allowed in this category (1-100)")
    channel_ids = fields.Many2many('slide.channel', string='Channels')
    website_id = fields.Many2one('website', string='Website')

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
            seq = self.env['ir.sequence'].next_by_code('lms.category.code')
            vals['code'] = f'CAT-{fields.Date.today().year}-{seq}'
        return super().create(vals)