# -*- coding: utf-8 -*-
{
    'name': 'Custom LMS Categories',
    'version': '18.0.1.0.0',
    'summary': 'Manage Learning Categories with Topics and Channels',
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
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/lms_category_views.xml',
        'views/slide_channel_views.xml',
        'views/menu_views.xml',
        'templates/categories_page.xml',
        'templates/homepage_ext.xml',
        'data/demo_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'custom_lms_categories/static/src/scss/categories.scss',
        ],
    },
    'demo': ['data/demo_data.xml'],
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
}