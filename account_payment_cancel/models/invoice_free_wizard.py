##############################################################################
#
#    Swiss localization Direct Debit module for OpenERP
#    Copyright (C) 2014 Compassion (http://www.compassion.ch)
#    @author: Cyril Sester <cyril.sester@outlook.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import models, api


class AccountInvoiceFree(models.TransientModel):

    ''' Wizard to free invoices. When job is done, user is redirected on new
        payment order.
    '''
    _name = 'account.invoice.free'

    @api.multi
    def invoice_free(self):
        inv_obj = self.env['account.invoice']
        invoices = inv_obj.browse(self.env.context.get('active_ids'))
        return invoices.cancel_payment_lines()
