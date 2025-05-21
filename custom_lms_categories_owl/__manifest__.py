

# -*- coding: utf-8 -*-
{
    'name': 'Custom LMS Categories OWL V2',
    'version': '18.0.1.0.0',
    'summary': 'V2 - Manage Learning Categories with Topics and Channels',
    'description': """
        Advanced category management for LMS with topic classification,
        tagging and channel association.
    """,
    'author': 'QuickStart2',
    'website': 'https://quickstart2.com',
    'category': 'eLearning',
    'depends': [
        'website',
        'website_slides',
        'rating',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/lms_category_views.xml',
        'views/slide_channel_views.xml',
        'views/menu_views.xml',
        'templates/categories_page.xml',
        'templates/homepage_ext.xml',
        'templates/course_templates.xml',
        'data/demo_data.xml',
        'templates/homepage_ext_V2.xml',
        'templates/components/category_card.xml',
        'templates/components/slider_section.xml',
        'templates/components/course_card.xml',
        'templates/components/modal_video.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'web/static/lib/jquery/jquery.js',
            # 'custom_lms_categories_owl/static/src/scss/categories.scss',
    #         # file built-in owl carousel
    #         # 'custom_lms_categories_owl/static/lib/owlcarousel/assets/owl.carousel.min.css',
    #         # 'custom_lms_categories_owl/static/lib/owlcarousel/assets/owl.theme.default.min.css',
    #         # 'custom_lms_categories_owl/static/lib/owlcarousel/owl.carousel.min.js',
    #         # custom pure js slider
    #         'custom_lms_categories_owl/static/src/js/slider_init.js',
    #         'custom_lms_categories_owl/static/src/scss/slider_styles.scss',
    #         'custom_lms_categories_owl/static/src/js/course_carousel.js',
    #         # Versione 2   
    #         'custom_lms_categories_owl/static/src/css/course_carousel.css',
    #         'custom_lms_categories_owl/static/src/js/owl_carousel_init_V2.js',
    #         'custom_lms_categories_owl/static/lib/owlcarousel/assets/owl.carouselV2.min.css',
    #     ],
    # },
    'demo': ['data/demo_data.xml'],
    #'images': ['static/description/icon.png'],
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
    "auto_install": False,
}


