from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LMSCategory(models.Model):
    _name = 'lms.category'
    _description = 'Learning Management System Category'
    _order = 'sequence, name asc'

    name = fields.Char(string='Category Name', required=True, translate=True)
    code = fields.Char(string='Code', copy=False, index=True)
    description = fields.Text(string='Description', translate=True)
    image_1920 = fields.Image(string='Cover Image', max_width=1920, max_height=1920)
    image_512 = fields.Image("Image 512", related='image_1920', max_width=512, max_height=512, store=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
    emoji = fields.Char(string='Emoji', default='📚', help="Emoji to represent the category")
    promote_on_home = fields.Boolean(string='Promote on Homepage', default=False)
    website_published = fields.Boolean(string='Published', default=True)
    item_limit = fields.Integer(
        string='Item Limit', 
        default=10, 
        help="Maximum items allowed in this category (1-100)"
    )
    
    # Relationships
    topic_ids = fields.Many2many('lms.topic', string='Related Topics')
    tag_ids = fields.Many2many('slide.channel.tag', string='Tags')
    channel_ids = fields.Many2many(
        'slide.channel', 
        string='Courses',
        relation='lms_category_slide_channel_rel',
        column1='category_id',
        column2='channel_id',
        domain=[('website_published', '=', True)],
        help="Published courses in this category"
    )
    featured_channel_ids = fields.Many2many(
        'slide.channel',
        string='Featured Courses',
        relation='lms_category_featured_channel_rel',
        column1='category_id',
        column2='channel_id',
        domain=[('website_published', '=', True)],
        help="Featured courses to display prominently"
    )
    
    website_id = fields.Many2one('website', string='Website')
    color = fields.Integer(string='Color Index')
    
    # Constraints and defaults
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
        return super().write(vals)

    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.code}] {record.name}" if record.code else record.name
            result.append((record.id, name))
        return result

    def get_website_channels(self, limit=12):
        """
        Get published channels for website display with limit
        """
        self.ensure_one()
        return self.channel_ids[:limit]

    @api.model
    def get_homepage_categories(self):
        """
        Get categories to display on homepage
        """
        return self.search([
            ('website_published', '=', True),
            ('promote_on_home', '=', True)
        ], order='sequence ASC')
    


class SlideChannelBadge(models.Model):
    _name = 'slide.channel.badge'
    _description = 'Corso Badge'

    code = fields.Char(string='Codice', required=True)
    name = fields.Char(string='Etichetta', required=True)
    color = fields.Char(string='Colore Sfondo', default='#FFFFFF', help="Hex color code for badge background")
    #color = fields.Integer(string="Colore Sfondo", default=0)
    description = fields.Text(string='Descrizione')
    main_badge = fields.Boolean(string='Principale', default=False)
    channel_id = fields.Many2one('slide.channel', string='Corso', ondelete='cascade')

    @api.constrains('main_badge')
    def _check_single_main_badge(self):
        for badge in self:
            if badge.main_badge:
                existing = self.search([
                    ('channel_id', '=', badge.channel_id.id),
                    ('main_badge', '=', True),
                    ('id', '!=', badge.id)
                ])
                if existing:
                    raise ValidationError(
                        _("Esiste già un badge principale per questo corso. Deseleziona l'altro o conferma la modifica.")
                    )



class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    # to refactor
    category_ids = fields.Many2many(
        'lms.category',
        relation='slide_channel_category_rel',
        column1='channel_id',
        column2='category_id',
        string='Categories',
        help="Categories this course belongs to"
    )

    # to refactor
    # Add fields for better display
    short_description = fields.Char(
        string='Short Description',
        compute='_compute_short_description',
        store=True
    )
    
    @api.depends('description')
    def _compute_short_description(self):
        for record in self:
            if record.description:
                record.short_description = record.description[:100] + '...' if len(record.description) > 100 else record.description
            else:
                record.short_description = ""

                    
    teaser_video_url = fields.Char(
        'Video Teaser URL',
        help="URL del video teaser (max 10 secondi) da mostrare come anteprima. Supporta YouTube e Vimeo."
    )

    
    landing_url = fields.Char(
        'URL Landing Page',
        help="URL della landing page esterna o interna."
    )

    # Relazione badge
    badge_ids = fields.One2many(
        'slide.channel.badge',
        'channel_id',
        string='Badge del corso'
    )
