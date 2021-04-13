# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Payment split',
    'version': '1.0',
    'category': 'Sale',
    'depends': ['account'],
    'data': [
        'account_view.xml',
        'wizard/wizard_view.xml',
    ],
    'demo': [
        ],
    'css': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
