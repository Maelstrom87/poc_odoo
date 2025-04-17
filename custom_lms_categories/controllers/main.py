from odoo import http

class LMSCategoryController(http.Controller):
    
    @http.route('/category/<int:category_id>', type='http', auth="public", website=True)
    def show_category(self, category_id, **kw):
        category = http.request.env['lms.category'].browse(category_id)
        return http.request.render('custom_lms_categories.public_categories_template', {
            'category': category
        })