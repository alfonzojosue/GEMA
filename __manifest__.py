{
    'name': 'GEMA - (Gestión Educativa y Matriculación Administrativa)',
    'description': 'Sistema de gestión educativa y matriculación administrativa',
    'category': 'Education',
    'version': '16.0.0.0.0',
    'license': 'AGPL-3',
    'author': 'Josue Alfonzo',
    'depends': [
        'base',
        'hr',
        'account',
        'product',
        'sale',
        'website',

    ],
    'data': [
        'security/ir.model.access.csv',
        'data/gema_payments_sequence.xml',
        'views/res_partnet_inherit.xml',
        'views/gema_subjects.xml',
        'views/gema_contracts.xml',
        'views/hr_employee_inherit.xml',
        'views/gema_payments.xml',
        'views/dashboard.xml',
        'views/dashboard_embebe.xml',
        'views/gema_menus.xml',
        'reports/contract_student.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'GEMA/static/src/**/*',
        ],
    },
    'application': True,
    'installable': True,
}