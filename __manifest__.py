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
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partnet_inherit.xml',
        'views/gema_subjects.xml',
        'views/gema_contracts.xml',
        'views/hr_employee_inherit.xml',
        'views/gema_menus.xml',
        'reports/contract_student.xml',
    ],
    'assets': {

    },
    'application': True,
    'installable': True,
}