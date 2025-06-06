from odoo import fields
from odoo import http
from odoo.http import request
import os
import logging
from odoo.addons.website_slides.controllers.main import WebsiteSlides

# Logger globale
_logger = logging.getLogger(__name__)

# Calcolo `module_name` una sola volta e lo rendo disponibile in tutto il modulo
MODULE_NAME = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_logger.info(f"Module name calculated: {MODULE_NAME}")


    #da verificare     
#    @http.route('/category/<int:category_id>', type='http', auth="public", website=True)
#    def show_category(self, category_id, **kw):
#        category = http.request.env['lms.category'].browse(category_id)
#        return http.request.render(f'{MODULE_NAME}.view_categories_page', {
#            'category': category
#        })
  


class LMSCategoryController(http.Controller):

    @http.route('/categories/<int:category_id>', type='http', auth="public", website=True)
    def show_category(self, category_id, **kw):
        _logger.info(f"Entering show_category with category_id: {category_id}")
        _logger.debug(f"Additional parameters received: {kw}")
        
        try:
            _logger.info("Attempting to browse lms.category with ID: %s", category_id)
            category = request.env['lms.category'].browse(category_id)
            
            if not category.exists():
                _logger.warning("Category with ID %s not found", category_id)
                return request.not_found()
                
            _logger.info("Found category: %s (ID: %s)", category.name, category.id)
            _logger.debug("Category data: %s", category.read())
            
            template_name = f'{MODULE_NAME}.category_page'
            _logger.info(f"Rendering template: {template_name}")
            
            return request.render(template_name, {
                'category': category,
                #'debug': True  # Aggiunto per abilitare debug nel template
            })
            
        except Exception as e:
            _logger.error("Error in show_category: %s", str(e), exc_info=True)
            raise


    # carousels netflix style
    @http.route('/lms/netflix', type='http', auth="public", website=True)
    def lms_nf_carousel(self):
         channels = http.request.env['slide.channel'].sudo().search([])
         return http.request.render(f'{MODULE_NAME}.online_course_carousel_view', {
             'channels': channels
         })

    # # carousels netflix style
    # @http.route('/lms/netflix/v2', type='http', auth="public", website=True)
    # def lms_nf_carousel_v2(self):
    #     channels = http.request.env['slide.channel'].sudo().search([])
    #     return http.request.render(f'{MODULE_NAME}.inherit_courses_home', {
    #         'channels': channels
    #     })
    # Netflix-style carousel route
    @http.route('/lms/netflix/v2', type='http', auth="public", website=True)
    def lms_nf_carousel_v2(self):
        _logger.info("Entering lms_nf_carousel_v2 route")
        
        try:
            _logger.info("Fetching all slide channels from the database")
            channels = request.env['slide.channel'].sudo().search([])
            
            _logger.info("Found %d channels", len(channels))
            _logger.info("Channels IDs: %s", channels.ids)

            template_name = f'{MODULE_NAME}.slider_v2_view'
            _logger.info(f"Rendering template: {template_name}")

            return request.render(template_name, {
                'channels': channels,
                #'debug': True  # Puoi attivare il debug nel template se necessario
            })

        except Exception as e:
            _logger.error("Error in lms_nf_carousel_v2: %s", str(e), exc_info=True)
            raise





class WebsiteSlidesExtended(WebsiteSlides):

    def get_course_ui_data(self, channel):
        main_badge = channel.badge_ids.filtered(lambda b: b.main_badge)
        other_badges = channel.badge_ids.filtered(lambda b: not b.main_badge)

        return {
            "id": channel.id,
            "name": channel.name,
            "image": f"/web/image/slide.channel/{channel.id}/image_512" if channel.image_1920 else "/path/to/placeholder.jpg",
            "price": "€49.99",  # eventualmente `channel.price` se esiste
            "total_slides": channel.total_slides,
            "total_time_hours": int(channel.total_time / 60) if channel.total_time else 0,
            "total_time_minutes": int(channel.total_time % 60) if channel.total_time else 0,
            "tags": channel.tag_ids.mapped('name'),
            "rating": round(channel.rating_avg or 4.7, 1),
            "is_new": channel.create_date and (fields.Datetime.now() - channel.create_date).days < 30,
            "main_badge": {
                "name": main_badge.name if main_badge else None,
                "color": main_badge.color if main_badge else None,
                "description": main_badge.description if main_badge else None,
            } if main_badge else None,
            "other_badges": [
                {
                    "name": b.name,
                    "color": b.color,
                    "description": b.description
                } for b in other_badges
            ],
            "cta": self.get_cta_label(channel),
            "card_hover_class": "hover:border-yellow-500",
            "icon_theme": "gold-on-black",
        }

    def get_cta_label(self, channel):
        user = request.env.user
        is_subscribed = self.is_user_subscribed_to_channel(channel)

        if is_subscribed:
            return {
                "caption": "Continua",
                "color": "bg-green-600 hover:bg-green-500",
                "url": f"/slides/channel/{channel.id}"
            }
        else:
            return {
                "caption": "Vai al corso",
                "color": "bg-red-700 hover:bg-red-600",
                "url": channel.landing_url or "#"
            }

    def is_user_subscribed_to_channel(self, channel):
        user = request.env.user
        partner_id = user.partner_id.id
        is_subscribed = request.env['slide.channel.partner'].search_count([
            ('partner_id', '=', partner_id),
            ('channel_id', '=', channel.id)
        ]) > 0
        return is_subscribed

    # @http.route(['/slides'], type='http', auth='user', website=True)
    # def courses(self, **kwargs):
    #     # Recupera tutti i canali pubblici
    #     domain = [('website_published', '=', True)]
    #     channels = request.env['slide.channel'].search(domain)
        
    #     # Trasforma in lista di dizionari UI-friendly
    #     channels_data = [self.get_course_ui_data(c) for c in channels]

    #     return request.render("website_slides.courses_home", {
    #         'channels': channels_data,  # sostituisce l'originale 'channels'
    #     })