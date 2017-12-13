from odoo.tests import TransactionCase
from odoo.modules import get_module_resource


class TestPaymentCancel(TransactionCase):

    def setUp(self):
        super(TestPaymentCancel, self).setUp()

        self.invoice_name = 'test invoice pain000'
        self.invoice_line_name = 'test invoice line pain000'
        self.order_name = '2017/1013'
        self.journal_name = '2017/1013'
        self.payment_line_name = 'Ltest'

        # Create payment order from the invoice
        invoice = self.env['account.invoice'].search(
            [('move_name', '=', self.invoice_name)])

        # Validate the invoice
        invoice.action_invoice_open()

        # Create a payment order
        action = invoice.create_account_payment_line()
        payment_order_id = action['res_id']

        payment_order = self.env['account.payment.order'].search(
            [('id', '=', payment_order_id)])

        partner_bank = self.env['account.journal'].search(
            [('name', '=', self.journal_name)])

        bank = self.env['account.journal'].search([('name', '=', 'Bank')])

        payment_order.name = self.order_name
        bank.update_posted = True

        payment_order.journal_id = partner_bank.id
        # Confirm payment order
        payment_order.draft2open()
        # Generate payment file
        payment_order.open2generated()
        # File successfully uploaded
        payment_order.generated2uploaded()

        payment_line = self.env['bank.payment.line'].search(
            [('order_id', '=', payment_order.id)])

        payment_line.name = self.payment_line_name


    #
        # self.env.cr.commit()
    #
    def test_invoice_exist(self):
        invoice = self.env['account.invoice'].search(
            [('move_name', '=', self.invoice_name)])

        self.assertTrue(invoice)

    def test_invoice_line_exist(self):
        invoice_line = self.env['account.invoice.line'].search(
            [('name', '=', self.invoice_line_name)])

        self.assertTrue(invoice_line)

    def test_invoice_state_is_paid(self):
        invoice = self.env['account.invoice'].search(
            [('move_name', '=', self.invoice_name)])

        self.assertEqual(invoice.state, 'paid')

    def test_payment_order_exist(self):
        payment_order = self.env['account.payment.order'].search(
            [('name', '=', self.order_name)])

        self.assertTrue(payment_order)

    def test_payment_order_state_is_uploaded(self):
        payment_order = self.env['account.payment.order'].search(
            [('name', '=', self.order_name)])

        self.assertEqual(payment_order.state, 'uploaded')

    def test_account_move_exist(self):
        payment_order = self.env['account.payment.order'].search(
            [('name', '=', self.order_name)])
        account_move = self.env['account.move'].search(
            [('payment_order_id', '=', payment_order.id)])

        self.assertTrue(account_move)

    def test_payment_line_exist(self):
        payment_line = self.env['bank.payment.line'].search(
            [('name', '=', self.payment_line_name)])

        # Check if there is a payment line
        self.assertTrue(payment_line)

    def test_account_move_deleted_after_free_invoice(self):
        self._invoice_free()

        payment_order = self.env['account.payment.order'].search(
            [('name', '=', self.order_name)])
        account_move = self.env['account.move'].search(
            [('payment_order_id', '=', payment_order.id)])

        self.assertFalse(account_move)

    def test_payment_order_state_is_cancel_after_free_invoice(self):
        self._invoice_free()

        payment_order = self.env['account.payment.order'].search(
            [('name', '=', self.order_name)])

        self.assertEqual(payment_order.state, 'cancel')

    def test_invoice_state_is_open_after_free_invoice(self):
        self._invoice_free()

        invoice = self.env['account.invoice'].search(
            [('move_name', '=', self.invoice_name)])

        self.assertEqual(invoice.state, 'open')


    #
    # def test_payment_line_deleted_after_import(self):
    #     self.import_file_pain000()
    #     payment_line = self.env['bank.payment.line'].search(
    #         [('name', '=', self.payment_line_name)])
    #
    #     # Check if there is a payment line
    #     self.assertFalse(payment_line)


    def _invoice_free(self):
        invoice = self.env['account.invoice'].search(
            [('move_name', '=', self.invoice_name)])

        free_wizard = self.env['account.invoice.free'].with_context(
            active_ids=invoice.ids).create({})
        free_wizard.invoice_free()
        # self.env.cr.commit()

