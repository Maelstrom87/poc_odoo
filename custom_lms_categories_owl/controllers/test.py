from odoo import http
from odoo.http import request
from odoo import fields
import os
import logging
import json

# Logger globale
_logger = logging.getLogger(__name__)

# Calcolo `module_name` una sola volta e lo rendo disponibile in tutto il modulo
MODULE_NAME = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_logger.info(f"Module name calculated: {MODULE_NAME}")

class TestController(http.Controller):

    #auth='user' assicura che solo utenti autenticati possano accedere.
    @http.route('/user/info', type='http', auth='user', website=True)
    def user_info(self, **kwargs):

        template_name = f'{MODULE_NAME}.user_info_template'
        user = request.env.user
        if user:
            groups = user.groups_id.mapped('name')
            
            _logger.info(f"Rendering template: {template_name}")
            return request.render(template_name, {
                'user': user,
                'groups': groups
            })
        else:
            return request.redirect('/web/login')


    #@http.route('/test/user-info', type='http', auth='user', website=True)
    @http.route('/test/user-info', type='http', auth='public', website=True)
    def user_extended_info(self, **kwargs):

        user = request.env.user
        partner = user.partner_id

        all_courses = request.env['slide.channel'].sudo().search([])

        template_name = f'{MODULE_NAME}.user_info_extended_template'

        user = request.env.user
        partner = user.partner_id

        # Corsi a cui è iscritto
        enrolled_courses = request.env['slide.channel'].search([
            ('partner_ids', 'in', partner.id)
        ])

        # Corsi acquistati (opzione base: prodotti di tipo corso acquistati)
        purchased_courses = request.env['slide.channel']
        if request.env['sale.order'].sudo().search_count([('partner_id', '=', partner.id)]):
            order_lines = request.env['sale.order.line'].sudo().search([
                ('order_id.partner_id', '=', partner.id),
                ('product_id.categ_id.name', 'ilike', 'corso')
            ])
            course_names = order_lines.mapped('product_id.name')
            purchased_courses = request.env['slide.channel'].sudo().search([
                ('name', 'in', course_names)
            ])

        _logger.info(f"Rendering template: {template_name}")
        #return request.render('your_module.user_info_extended_template', {
        return request.render(template_name, {
            'user': user,
            'enrolled_courses': enrolled_courses,
            'purchased_courses': [],  # se differente, puoi filtrare da sale.order
            'all_courses': all_courses,
            'json': json,  # passa json nel contesto per poter usare json.dumps nel template
            
        })


    #modificare auth solo per admin (test)
    #@http.route('/test/card/uidata', type='http', auth='user', website=True)    
    @http.route('/test/card/uidata', type='http', auth="public", website=True)
    def test_card_ui_data(self):
        _logger.info("Loading Test Card UI Data")
        template_name = f'{MODULE_NAME}.test_card_uidata_template'

        try:

            channels = request.env['slide.channel'].sudo().search([])
            helper = TestController()
            course_cards = [helper.get_course_ui_data(ch) for ch in channels]

            return request.render(template_name, {
                'course_cards': course_cards
            })

        except Exception as e:
            _logger.error("Error Test Card UI Data: %s", str(e), exc_info=True)
            raise


    def get_course_ui_data(self, channel):
        main_badge = channel.badge_ids.filtered(lambda b: b.main_badge)
        other_badges = channel.badge_ids.filtered(lambda b: not b.main_badge)

        return {

            #[01] Dati base del corso
            "id": channel.id,
            "name": channel.name,
            #da verificare gestion immagine
            "image": f"/web/image/slide.channel/{channel.id}/image_512" if channel.image_1920 else "/path/to/placeholder.jpg",
            #da verificare dove prendere il prezzo 
            "price": "€49.99",

            #[02] Statistiche del corso
            "total_slides": channel.total_slides,
            "total_time_hours": int(channel.total_time / 60) if channel.total_time else 0,
            "total_time_minutes": int(channel.total_time % 60) if channel.total_time else 0,
            #"total_views": channel.total_views or 0,
            "tags": channel.tag_ids.mapped('name'),
            "rating": round(channel.rating_avg or 4.7, 1),
            #[mata informazioni] eventualmente per una sezione Novità
            "is_new": channel.create_date and (fields.Datetime.now() - channel.create_date).days < 30,
            
            #[03] Badge del corso
            # Se il badge principale non esiste, restituisce None
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

            #[04] Informazioni aggiuntive: CTA dinamiche
            #da miglorare
            "cta_caption": self.get_cta_label(channel),
            "cta_class": "bg-red-700 hover:bg-red-600",


            #[05] Informazioni di visualizzazione dinamice: da verificare con Diego quali gestire e come
            "card_hover_class": "hover:border-yellow-500",
            "icon_theme": "gold-on-black",
            
            
        }


        # def get_cta_label(self, channel):
        #     user = request.env.user
        #     if channel.id in user.channel_subscription_ids.mapped('channel_id').ids:
        #         return "Continua"
        #     else:
        #         return "Vai al corso

    def get_cta_label(self, channel):
        user = request.env.user
        #is_subscribed = channel.id in user.channel_subscription_ids.mapped('channel_id').ids
        #is_subscribed = self.is_user_subscribed_to_channel(user, channel)
        is_subscribed = self.is_user_subscribed_to_channel(channel)

        if is_subscribed:
            return {
                "caption": "Continua",
                "color": "bg-green-600 hover:bg-green-500",
                "url": f"/slides/channel/{channel.id}"  # URL alla pagina del corso
            }
        else:
            return {
                "caption": "Vai al corso",
                "color": "bg-red-700 hover:bg-red-600",
                "url": channel.landing_url or "#"  # Fallback se la landing_url non è definita
            }


    #valutare come gestire l’accesso ACL senza sudo() in PROD
    def is_user_subscribed_to_channel(self, channel):
        user = request.env.user
        partner_id = user.partner_id.id

        is_subscribed = request.env['slide.channel.partner'].search_count([
                ('partner_id', '=', partner_id),
                ('channel_id', '=', channel.id)
            ]) > 0
        _logger.info("User %s subscription to channel %s: %s", user.id, partner_id, channel.id, is_subscribed)
        return is_subscribed



    # def is_user_subscribed_to_channel(self, channel):
    #     user = request.env.user
    #     is_subscribed = request.env['slide.channel.partner'].search_count([
    #         ('user_id', '=', user.id),
    #         ('channel_id', '=', channel.id)
    #     ]) > 0
    #     _logger.info("User %s subscription to channel %s: %s", user.id, channel.id, is_subscribed)
    #     return is_subscribed


    # def is_user_subscribed_to_channel(self, user, channel):
    #     """
    #     Verifica se l'utente è iscritto al canale (corso).
    #     :param user: istanza di res.users
    #     :param channel: istanza di slide.channel
    #     :return: True se iscritto, False altrimenti
    #     """
    #     return request.env['slide.channel.partner'].sudo().search_count([
    #         ('user_id', '=', user.id),
    #         ('channel_id', '=', channel.id)
    #     ]) > 0