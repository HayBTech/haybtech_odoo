{
    'name': 'HayBTech Payment Provider',
    'version': '1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Acceptez les paiements Mobile Money (Orange, Wave, Free) via HayBTech.',
    'author': 'HayBTech Team',
    'depends': ['payment'],
    'data': [
        'views/payment_provider_views.xml',
        'views/payment_haybtech_templates.xml',
        'data/payment_provider_data.xml',
    ],
    'application': False,
    'license': 'LGPL-3',
}
