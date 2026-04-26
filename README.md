# HayBTech for Odoo

Official Odoo payment provider module for HayBTech -- accept Orange Money, Wave, Free Money, MTN MoMo, Moov Flooz, and TMoney in your Odoo eCommerce and Point of Sale.

[![Odoo](https://img.shields.io/badge/Odoo-16%20%7C%2017-714B67.svg)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-LGPL--3-green)](LICENSE)

---

## Features

- Native Odoo payment provider integration
- Seamless redirect to HayBTech hosted payment page
- Automatic webhook verification with HMAC-SHA256 signature validation
- Full support for Test and Live modes
- Embedded Python SDK (zero external pip dependencies)
- Compatible with Odoo eCommerce, Point of Sale, and Invoicing

---

## Requirements

| Requirement | Version       |
|:------------|:--------------|
| Odoo        | 16.0 or 17.0 |
| Python      | 3.8+          |

**Odoo module dependencies:** `payment`

---

## Installation

1. Copy the `haybtech_odoo` directory to your Odoo addons path:

```bash
cp -r haybtech_odoo/ <odoo-root>/addons/haybtech_odoo/
```

2. Restart the Odoo server:

```bash
sudo systemctl restart odoo
```

3. In the Odoo admin, go to **Apps**, remove the "Apps" filter, search for **HayBTech Payment Provider**, and click **Install**.

---

## Configuration

1. Go to **Invoicing > Configuration > Payment Providers** (or **Website > Configuration > Payment Providers**).
2. Select **HayBTech**.
3. Configure:

| Field              | Description                                    |
|:-------------------|:-----------------------------------------------|
| **State**          | Test or Live                                   |
| **Secret Key**     | Your `sk_test_...` or `sk_live_...` key        |
| **Webhook Secret** | Your `whsec_...` signing secret                |

4. Click **Save**.

---

## Webhook Setup

1. In your **HayBTech Dashboard**, go to **Settings > Webhooks**.
2. Add a new endpoint:

```
https://your-odoo.com/payment/haybtech/webhook
```

3. Copy the webhook secret into the Odoo provider configuration.

---

## How It Works

1. Customer selects **HayBTech** during checkout.
2. Odoo creates the transaction and redirects to the HayBTech payment page.
3. Customer pays via their preferred mobile money provider.
4. HayBTech sends a signed webhook to your Odoo instance.
5. The module verifies the signature and confirms the transaction.
6. Customer is redirected back to the Odoo confirmation page.

---

## Supported Providers

| Provider       | Countries           |
|:---------------|:--------------------|
| Orange Money   | SN, CI, ML, BF, GW |
| Wave           | SN, CI, ML, BF     |
| Free Money     | SN                  |
| MTN MoMo       | CI, BJ              |
| Moov Flooz     | BJ, TG, NE, BF     |
| TMoney         | TG                  |

---

## Module Structure

```
haybtech_odoo/
  __manifest__.py                # Module metadata and dependencies
  models/                        # Odoo model overrides
  sdk/                           # Embedded HayBTech Python SDK
    __init__.py
    client.py                    # HTTP client with auth and security
    webhook.py                   # HMAC-SHA256 signature verification
    resources/
      payments.py                # Payments resource
      webhooks.py                # Webhooks resource
```

---

## Security

- **HMAC-SHA256 Webhook Verification** with constant-time comparison
- **Zero pip Dependencies** -- embedded SDK uses only Python stdlib
- **Secret Masking** in logs and `repr()` output
- **1 MB Payload Limit** to prevent memory exhaustion
- **CRLF Guard** against HTTP header injection
- **Replay Protection** -- 5-minute timestamp tolerance on signatures

---

## Troubleshooting

| Issue                   | Solution                                                      |
|:------------------------|:--------------------------------------------------------------|
| Module not appearing    | Update the apps list and remove the "Apps" filter             |
| Provider not available  | Ensure the `payment` module is installed                      |
| Webhooks returning 403  | Verify webhook secret matches the HayBTech dashboard          |
| Transactions pending    | Check Odoo server logs for webhook processing errors          |

---

LGPL-3 License
