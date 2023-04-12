{
    'name': 'Move Order',
    'version': '16',
    'summary': 'Inventory - Move Order',
    'description': """
        Submenu baru pada menu Inventory yang memiliki fitur untuk memindahkan product antar warehouse dan lokasi
    """,
    "category": "Inventory",
    'author': 'Muhammad Azis - 087881071515',
    'company': 'Ismata Nusantara Abadi',
    'website': "https://www.ismata.co.id",
    'depends': ['base', 'stock', 'mail', 'mrp'],
    'data': [
        'reports/report_move_order.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/view.xml',
        'views/res_config_views.xml',
        'views/scrap_views.xml',
        'views/action_report.xml',
    ],
    'images': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
