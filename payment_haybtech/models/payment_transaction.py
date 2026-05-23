import logging
import werkzeug
from werkzeug import urls

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

# Import SDK
from ..sdk import HayBTechClient

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """ Override of payment to return HayBTech-specific rendering values. """
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'haybtech':
            return res

        base_url = self.provider_id.get_base_url()
        return_url = urls.url_join(base_url, '/payment/haybtech/return')

        try:
            # Initialize SDK
            secret_key = self.provider_id._haybtech_get_secret_key()
            client = HayBTechClient(secret_key)

            # Create Payment
            payment_response = client.payments.create({
                'merchant_ref': self.reference,
                'amount': int(self.amount),
                'currency': self.currency_id.name,
                'return_url': return_url,
                'cancel_url': return_url
            })

            if payment_response.get('status') == 'success' and 'payment_url' in payment_response.get('data', {}):
                payment_url = payment_response['data']['payment_url']
                # Odoo will use 'api_url' for standard redirect
                res.update({
                    'api_url': payment_url,
                })
            else:
                raise ValidationError(_("HayBTech: Failed to generate payment URL."))

        except Exception as e:
            _logger.error(f"HayBTech API Error: {str(e)}")
            raise ValidationError(_("HayBTech: Error communicating with the payment provider."))

        return res

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """ Override to find the transaction based on HayBTech webhook data. """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'haybtech' or len(tx) == 1:
            return tx

        merchant_ref = notification_data.get('merchant_ref')
        if not merchant_ref:
            raise ValidationError(_("HayBTech: Missing merchant_ref in notification data."))

        tx = self.search([('reference', '=', merchant_ref), ('provider_code', '=', 'haybtech')])
        if not tx:
            raise ValidationError(_("HayBTech: No transaction found matching reference %s.", merchant_ref))

        return tx

    def _process_notification_data(self, notification_data):
        """ Override to process HayBTech webhook/return data. """
        super()._process_notification_data(notification_data)
        if self.provider_code != 'haybtech':
            return

        status = notification_data.get('status')
        
        if status == 'success':
            # Double check with API for extra security if it's from a return URL
            # But the webhook signature already validates this.
            self._set_done()
        elif status == 'failed':
            self._set_error(_("HayBTech: Payment failed."))
        elif status == 'cancelled':
            self._set_canceled()
        else:
            self._set_pending()
