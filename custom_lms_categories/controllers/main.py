from odoo import http
from odoo.http import request
import os
import logging

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