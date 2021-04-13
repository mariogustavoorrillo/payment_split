from odoo import tools,fields, models, api, _
from datetime import date
from odoo.exceptions import ValidationError
from odoo.tools import float_is_zero

class AccountPayment(models.Model):
    _inherit = 'account.payment'


    def btn_split_payment(self):
        self.ensure_one()
        if self.state not in ['posted']:
            raise ValidationError('El estado del documento es incorrecto')
        if self.payment_type not in ['inbound']:
            raise ValidationError('El tipo del documento es incorrecto')
        if self.split_move_lines:
            raise ValidationError('Pago ya particionado')
        wizard_id = self.env['payment.split.wizard'].create({'payment_id': self.id})
        return {
               'name': _('Fraccionar pago'),
               'res_model': 'payment.split.wizard',
               'res_id': wizard_id.id,
               'view_mode': 'form',
               'type': 'ir.actions.act_window',
               'target': 'new',
               }

    split_move_lines = fields.One2many(comodel_name='account.move.line',inverse_name='split_payment_id',string='Split payments')


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    split_payment_id = fields.Many2one('account.payment',string='Split Payment')
