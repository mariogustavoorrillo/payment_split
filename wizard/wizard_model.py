from odoo import fields,models, api, _
from odoo.exceptions import UserError, ValidationError


class PaymentSplitWizard(models.TransientModel):
    _name = "payment.split.wizard"
    _description = "payment.split.wizard"

    def btn_confirm(self):
        if not self.payment_id or not self.journal_id:
            raise ValidationError('Debe seleccionar un diario')
        total_amount = self.payment_id.amount
        line_amount = 0
        for line in self.line_ids:
            line_amount = line_amount + line.amount
        if line_amount != total_amount:
            raise ValidationError('Debe ingresar los montos exactos')
        payment_move_line = self.env['account.move.line']
        for move_line in self.payment_id.move_line_ids:
            if move_line.account_id.reconcile:
                payment_move_line += move_line
        if not payment_move_line:
            raise ValidationError('No se pudo determinar la linea a conciliar')
        vals_move = {
                'journal_id': self.journal_id.id,
                'type': 'entry',
                'ref': 'SPLIT ' + str(self.payment_id.display_name),
                }
        move_id = self.env['account.move'].with_context(check_move_validity=False).create(vals_move)
        vals_debit = {
            'split_payment_id': self.payment_id.id,
            'move_id': move_id.id,
            'debit': total_amount,
            'partner_id': self.payment_id.partner_id.id,
            'account_id': payment_move_line[0].account_id.id,
            'name': 'Particion pago DR %s'%(self.payment_id.display_name),
            }
        debit_id = self.env['account.move.line'].with_context(check_move_validity=False).create(vals_debit)
        for line_amount in self.line_ids:
            vals_credit = {
                'split_payment_id': self.payment_id.id,
                'move_id': move_id.id,
                'credit': line_amount.amount,
                'partner_id': self.payment_id.partner_id.id,
                'account_id': payment_move_line[0].account_id.id,
                'name': 'Particion pago CR %s'%(self.payment_id.display_name),
                }
            credit_id = self.env['account.move.line'].with_context(check_move_validity=False).create(vals_credit)
        move_id.post()
        payment_move_line += debit_id
        payment_move_line.reconcile()


        

    payment_id = fields.Many2one(comodel_name='account.payment',string='Pago')
    journal_id = fields.Many2one('account.journal',string='Diario')
    line_ids = fields.One2many(comodel_name='payment.split.wizard.line',inverse_name='wizard_id',string='Lineas')


class PaymentSplitWizardLine(models.TransientModel):
    _name = 'payment.split.wizard.line'
    _description = 'payment.split.wizard.line'

    wizard_id = fields.Many2one('payment.split.wizard',string='Wizard')
    amount = fields.Float('Monto')
