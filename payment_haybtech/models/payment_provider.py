import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('haybtech', "HayBTech")], ondelete={'haybtech': 'set default'}
    )

    haybtech_test_secret_key = fields.Char(
        string="Test Secret Key",
        help="The test secret key from your HayBTech dashboard",
        required_if_provider='haybtech',
        groups='base.group_system'
    )
    haybtech_live_secret_key = fields.Char(
        string="Live Secret Key",
        help="The live secret key from your HayBTech dashboard",
        required_if_provider='haybtech',
        groups='base.group_system'
    )
    haybtech_webhook_secret = fields.Char(
        string="Webhook Secret",
        help="The webhook secret from your HayBTech dashboard",
        required_if_provider='haybtech',
        groups='base.group_system'
    )

    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['haybtech'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res

    def _get_supported_currencies(self):
        """ Override of payment to return the supported currencies. """
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'haybtech':
            # Support XOF for now, or fetch from DB
            xof_currency = self.env['res.currency'].search([('name', '=', 'XOF')], limit=1)
            if xof_currency:
                supported_currencies |= xof_currency
        return supported_currencies

    def _haybtech_get_secret_key(self):
        self.ensure_one()
        return self.haybtech_test_secret_key if self.state == 'test' else self.haybtech_live_secret_key
