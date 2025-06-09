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
        'web',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/lms_category_views.xml',
        'views/slide_channel_views.xml',
        'views/menu_views.xml',
        'data/demo_data.xml',
        'templates/test_card_uidata.xml',
        'templates/test.xml',
        'templates/homepage_ext_swiper.xml',
        'templates/components/category_card.xml',
        'templates/components/slider_section_swiper.xml',
        'templates/components/swiper_course_card.xml',
        'templates/components/modal_video_v1.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_lms_categories/static/src/css/lms_swiper.css',
            'custom_lms_categories/static/src/js/swiper_init.js',
        ],
    },
    'demo': ['data/demo_data.xml'],
    'application': True,
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
}


