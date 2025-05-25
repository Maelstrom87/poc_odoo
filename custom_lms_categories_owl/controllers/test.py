from odoo import http
from odoo.http import request
import os
import logging

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


    @http.route('/user/extended-info', type='http', auth='user', website=True)
    def user_extended_info(self, **kwargs):

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
            'purchased_courses': purchased_courses
        })
