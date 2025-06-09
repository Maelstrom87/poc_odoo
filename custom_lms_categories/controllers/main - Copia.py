import json
from odoo import http, _
from odoo.http import request
import os
import logging
from odoo.addons.website_slides.controllers.main import WebsiteSlides

_logger = logging.getLogger(__name__)
MODULE_NAME = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class LMSCategoryController(http.Controller):

    @http.route('/categories/<int:category_id>', type='http', auth="public", website=True)
    def show_category(self, category_id, **kw):
        _logger.info(f"Entering show_category with category_id: {category_id}")
        try:
            category = request.env['lms.category'].browse(category_id)
            if not category.exists():
                return request.not_found()
            return request.render(f'{MODULE_NAME}.category_page', {'category': category})
        except Exception as e:
            _logger.error("Error in show_category: %s", str(e), exc_info=True)
            raise

    @http.route('/lms/netflix', type='http', auth="public", website=True)
    def lms_nf_carousel(self):
        channels = request.env['slide.channel'].sudo().search([])
        return request.render(f'{MODULE_NAME}.online_course_carousel_view', {
            'channels': channels
        })

    @http.route('/lms/netflix/v2', type='http', auth="public", website=True)
    def lms_nf_carousel_v2(self):
        try:
            channels = request.env['slide.channel'].sudo().search([])
            return request.render(f'{MODULE_NAME}.slider_v2_view', {
                'channels': channels,
            })
        except Exception as e:
            _logger.error("Error in lms_nf_carousel_v2: %s", str(e), exc_info=True)
            raise



@http.route('/lms/get_channel_data', type='json', auth="public", website=True, csrf=False)
def get_channel_data(self, channel_id, **kw):
    """Endpoint JSON per i dati della modale"""
    try:
        channel = request.env['slide.channel'].browse(int(channel_id))
        if not channel.exists():
            return {'error': 'Channel not found'}

        is_subscribed = self._is_user_subscribed_to_channel(channel)

        return {
            'name': channel.name,
            'description': channel.description or '',
            'short_description': channel.short_description or '',
            'prezzo_in_euro': channel.prezzo_in_euro or '0',
            'prezzo_in_franchi': channel.prezzo_in_franchi or '0',
            'descrizione_prezzo': channel.descrizione_prezzo or '',
            'tag_ids': [{'name': tag.name} for tag in channel.tag_ids],
        }
    except Exception as e:
        _logger.error("Error in get_channel_data: %s", str(e))
        return {'error': str(e)}



# @http.route('/lms/get_channel_data', type='json', auth="public", website=True, csrf=False)
# def get_channel_data(self, channel_id, **kw):
#     """Endpoint JSON per i dati della modale"""
#     try:
#         channel = request.env['slide.channel'].browse(int(channel_id))
#         if not channel.exists():
#             return {'error': 'Channel not found'}

#         is_subscribed = self._is_user_subscribed_to_channel(channel)

#         return {
#             'name': channel.name,
#             'description': channel.description or '',
#             'short_description': channel.short_description or '',
#             'prezzo_in_euro': channel.prezzo_in_euro or '0',
#             'prezzo_in_franchi': channel.prezzo_in_franchi or '0',
#             'descrizione_prezzo': channel.descrizione_prezzo or '',
#             'tag_ids': [{'name': tag.name} for tag in channel.tag_ids],
#             'cta': {
#                 'caption': self._get_cta_caption(channel),
#                 'color': self._get_cta_color(channel, is_subscribed),
#                 'url': self._get_cta_url(channel),
#             },
#         }
#     except Exception as e:
#         _logger.error("Error in get_channel_data: %s", str(e))
#         return {'error': str(e)}



def _is_user_subscribed_to_channel(self, channel):
        """Verifica se l'utente è iscritto al canale"""
        if request.env.user._is_public():
            return False
        return bool(request.env['slide.channel.partner'].search_count([
            ('partner_id', '=', request.env.user.partner_id.id),
            ('channel_id', '=', channel.id)
        ]))

def _get_cta_color(self, channel, is_subscribed):
        """Restituisce la classe Tailwind per lo stato del CTA"""
        return "text-white bg-green-600 hover:bg-green-500" if is_subscribed else "bg-blue-700 hover:bg-blue-600"

def _get_cta_url(self, channel):
        """Restituisce l'URL appropriato in base allo stato"""
        if self._is_user_subscribed_to_channel(channel):
            return f"/slides/{channel.id}"
        return channel.landing_url or "#"

def _get_cta_caption(self, channel):
        """Restituisce la caption appropriata in base allo stato"""
        if self._is_user_subscribed_to_channel(channel):
            return _("Vai al Corso")
        return _("Scopri il corso")