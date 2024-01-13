{
    'name' : 'Modulo de Ropa',
    'version' : '1.0',
    'depends' : ['base', 'account', 'contacts'],
    'author' : 'Asel Fernandez',
    'category': 'Ropa',
    'website' : '',
    'description' : '''Módulo para gestionar una tienda de ropa''',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/categoria.xml',
        'views/menu.xml',
        'wizard/update_wizard_view.xml',
        'data/numero_compra.xml',
        'views/ropa_view.xml',
        'views/compra_view.xml',
    ],
}