import re
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

#     channel_ids = fields.Many2many(
#         'slide.channel',
#         'slide_channel_category_rel',  # <-- usa la stessa tabella
#         'category_id',                 # <-- deve essere il campo opposto rispetto all'altro modello
#         'channel_id',
#         string='Courses',
#         domain=[('website_published', '=', True)],
#         help="Published courses in this category"
#     )

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

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('code'):
                seq = self.env['ir.sequence'].next_by_code('lms.category.code') or '000'
                vals['code'] = f'CAT-{fields.Date.today().year}-{seq[-3:]}'
        return super().create(vals_list)

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
    background_color = fields.Char(string='Colore Sfondo', default='#FFFFFF', help="Hex color code for badge background")
    color = fields.Char(string='Colore testo', default='#000000', help="Hex color code for badge text")
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



from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    category_ids = fields.Many2many(
        'lms.category',
        relation='slide_channel_category_rel',
        column1='channel_id',
        column2='category_id',
        string='Categories',
        help="Categories this course belongs to"
    )

    badge_ids = fields.One2many(
        'slide.channel.badge',
        'channel_id',
        string='Badge del corso'
    )

    tag_ids = fields.Many2many('slide.channel.tag', string='Tags')


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

    prezzo_in_euro = fields.Float(
        string='Prezzo in Euro',
        digits=(12, 2),  # 12 cifre totali, 2 decimali
        help='Prezzo del corso in Euro'
    )
    
    prezzo_in_franchi = fields.Float(
        string='Prezzo in Franchi Svizzeri',
        digits=(12, 2),
        help='Prezzo del corso in Franchi Svizzeri'
    )
    
    descrizione_prezzo = fields.Text(
        string='Descrizione Prezzo',
        help='Descrizione dettagliata del prezzo e eventuali condizioni'
    )


    # [sezione teaser video] ================================================
    teaser_video_url = fields.Char(
        'Video Teaser URL',
        help="URL del video teaser (max 10 secondi) da mostrare come anteprima. Supporta YouTube e Vimeo."
    )

    teaser_video_embed_url = fields.Char(
        'Video Teaser Embed URL',
        compute='_compute_teaser_video_embed_url',
        store=True
    )

    @api.depends('teaser_video_url')
    def _compute_teaser_video_embed_url(self):
        for record in self:
            if not record.teaser_video_url:
                record.teaser_video_embed_url = False
                continue
                
            # Handle Vimeo URLs
            if 'vimeo.com/' in record.teaser_video_url:
                video_id = record.teaser_video_url.split('vimeo.com/')[-1].split('?')[0]
                record.teaser_video_embed_url = f'https://player.vimeo.com/video/{video_id}'
            # Handle YouTube URLs
            elif 'watch?v=' in record.teaser_video_url:
                record.teaser_video_embed_url = record.teaser_video_url.replace("watch?v=", "embed/")
            # Handle youtu.be URLs
            elif 'youtu.be/' in record.teaser_video_url:
                video_id = record.teaser_video_url.split('youtu.be/')[-1].split('?')[0]
                record.teaser_video_embed_url = f'https://www.youtube.com/embed/{video_id}'
            else:
                record.teaser_video_embed_url = record.teaser_video_url

    @api.constrains('teaser_video_url')
    def _check_teaser_video_url(self):
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|vimeo)\.(com|be|org)/'
        )
        for channel in self:
            if channel.teaser_video_url and not youtube_regex.match(channel.teaser_video_url):
                raise ValidationError(_("L'URL del teaser deve essere un link a YouTube o Vimeo."))

    landing_url = fields.Char(
        'URL Landing Page',
        help="URL della landing page esterna o interna."
    )


# Metodi per la gestione della UI
    #@api.model # metodo "statico" che non dipende da record specifici
    def get_course_ui_data(self, user=None):
        """Versione migliorata che può essere chiamata anche da contesti non-web"""
        self.ensure_one()
        user = user or self.env.user
        return {
            **self._get_course_base_data(),
            **self._get_user_specific_data(user)
        }

    # metodo privato prefixato con "_" per indicare che è interno alla classe
    def _get_course_base_data(self):
        """Dati indipendenti dall'utente"""
        self.ensure_one()
        main_badge = self.badge_ids.filtered(lambda b: b.main_badge)
        other_badges = self.badge_ids.filtered(lambda b: not b.main_badge)

        return {
            "id": self.id,
            "name": self.name,
            "image": f"/web/image/slide.channel/{self.id}/image_512" if self.image_1920 else "/path/to/placeholder.jpg",
            "price": "€49.99",
            "total_slides": self.total_slides,
            "total_time_hours": int(self.total_time / 60) if self.total_time else 0,
            "total_time_minutes": int(self.total_time % 60) if self.total_time else 0,
            "tags": self.tag_ids.mapped('name'),
            "rating": round(self.rating_avg or 4.7, 1),
            "is_new": self.create_date and (fields.Datetime.now() - self.create_date).days < 30,
            "main_badge": {
                "name": main_badge.name,
                "color": main_badge.color,
                "background_color": main_badge.background_color,
                "description": main_badge.description
            } if main_badge else None,
            "other_badges": [{
                "name": b.name,
                "color": b.color,
                "background_color": b.background_color,
                "description": b.description
            } for b in other_badges],
            "card_hover_class": "hover:border-yellow-500",
            "icon_theme": "gold-on-black",
        }

    # metodo privato prefixato con "_" per indicare che è interno alla classe
    def _get_user_specific_data(self, user):
        """Dati dipendenti dall'utente"""
        self.ensure_one()
        return {
            "cta": self._get_cta_label(user)
        }

    # metodo privato prefixato con "_" per indicare che è interno alla classe
    def _get_cta_label(self, user):
        """Genera il CTA in base allo stato dell'utente"""
        self.ensure_one()
        is_subscribed = self._is_user_subscribed(user)
        
        return {
            "caption": _("Vai al Corso") if is_subscribed else _("Scopri il corso"),
            "color": "text-white bg-green-600 hover:bg-green-500" if is_subscribed else "bg-blue-700 hover:bg-blue-600",
            # "color": "text-white bg-green-600 hover:bg-green-500" if is_subscribed else "text-white bg-[var(--accent-color)] hover:bg-[var(--background-dark)]",
            "url": f"/slides/{self.id}" if is_subscribed else (self.landing_url or "#")
            # '/slides/' + str(channel.id)
        }

    def _is_user_subscribed(self, user):
        """Verifica se l'utente è iscritto al corso"""
        self.ensure_one()
        return bool(self.env['slide.channel.partner'].search_count([
            ('partner_id', '=', user.partner_id.id),
            ('channel_id', '=', self.id)
        ]))
    

    