import logging
import pprint
import json

from odoo import http
from odoo.http import request
from odoo.exceptions import ValidationError

from ..sdk.webhook import Webhook

_logger = logging.getLogger(__name__)

class HayBTechController(http.Controller):
    _return_url = '/payment/haybtech/return'
    _webhook_url = '/payment/haybtech/webhook'

    @http.route(_return_url, type='http', auth='public', methods=['GET'], csrf=False)
    def haybtech_return(self, **post):
        """ The return URL when the user is redirected back from the payment gateway. """
        _logger.info("HayBTech Return Data: %s", pprint.pformat(post))
        
        # If the URL contains status params, process them.
        # Ideally, we verify the transaction directly via API if status is not provided securely.
        if 'merchant_ref' in post:
            request.env['payment.transaction'].sudo()._handle_notification_data('haybtech', post)
        
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def haybtech_webhook(self, **post):
        """ The webhook URL where HayBTech sends asynchronous payment updates. """
        payload = request.httprequest.data.decode('utf-8')
        signature = request.httprequest.headers.get('X-HayBTech-Signature')
        
        if not signature:
            return request.make_response("Missing Signature", status=403)

        # Get the HayBTech provider to retrieve the webhook secret
        provider = request.env['payment.provider'].sudo().search([('code', '=', 'haybtech')], limit=1)
        if not provider or not provider.haybtech_webhook_secret:
            return request.make_response("Provider Configuration Error", status=500)

        try:
            # Secure verification using the SDK
            event = Webhook.construct_event(
                payload=payload,
                signature_header=signature,
                secret=provider.haybtech_webhook_secret
            )

            # Reformat event data to match what _get_tx_from_notification_data expects
            event_data = event.get('data', {})
            notification_data = {
                'merchant_ref': event_data.get('merchant_ref'),
                'status': event_data.get('status'),
                'amount': event_data.get('amount'),
                'currency': event_data.get('currency'),
            }

            request.env['payment.transaction'].sudo()._handle_notification_data('haybtech', notification_data)
            return request.make_response("OK", status=200)

        except Exception as e:
            _logger.error("HayBTech Webhook Error: %s", str(e))
            return request.make_response("Invalid Signature", status=403)
