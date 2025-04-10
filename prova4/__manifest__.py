# __manifest__.py
{
    "name": "PROVA4",
    "version": "1.0",
        'summary': 'Diegone',
    'website': 'https://www.odoo.com/app/diego',
    'depends': ['base'],
    "depends": ["base", "web"],
    "data": [
        "views/custom_views.xml",  # File XML della vista
        'security/ir.model.access.csv',
                "views/menu.xml",

    ],

    "assets": {
        "web.assets_backend": [
            "prova4/static/src/js/custom_owl_component.js",  # File JavaScript del componente OWL
            "prova4/static/src/xml/custom_owl_templates.xml",  # File XML del template OWL
        ],
    },
    "application":True,
        'installable': True,

}