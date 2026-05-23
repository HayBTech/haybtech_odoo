# HayBTech for PrestaShop

Official PrestaShop payment module for HayBTech -- accept mobile money payments on your PrestaShop store.

[![PrestaShop](https://img.shields.io/badge/PrestaShop-1.7%20%7C%208.x-DF0067.svg)](https://www.prestashop.com/)
[![PHP](https://img.shields.io/badge/PHP-8.1+-blue.svg)](https://php.net/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Features

- Native PrestaShop payment module with admin configuration panel
- Seamless redirect to HayBTech hosted payment page
- Automatic webhook verification with HMAC-SHA256 signature validation
- Full support for Test and Live modes
- Zero external Composer dependencies (embedded SDK)

---

## Requirements

| Requirement | Version           |
|:------------|:------------------|
| PrestaShop  | 1.7.x or 8.x     |
| PHP         | 8.1+              |

---

## Installation

### Via Back Office

1. Download the module as a `.zip` archive.
2. Go to **Modules > Module Manager > Upload a module**.
3. Select the `.zip` file -- the module installs automatically.

### Manual

```bash
cp -r haybtech-prestashop/ <prestashop-root>/modules/haybtech/
```

Then install via admin: **Modules > Module Manager > HayBTech > Install**.

---

## Configuration

1. Go to **Modules > Module Manager > HayBTech > Configure**.
2. Fill in your **Secret Key** and **Webhook Secret** from the HayBTech dashboard.
3. Toggle **Test Mode** as needed, then click **Save**.

---

## Webhook Setup

Add this endpoint in your **HayBTech Dashboard > Settings > Webhooks**:

```
https://your-store.com/module/haybtech/webhook
```

---

## How It Works

1. Customer selects **Payer par Mobile Money (HayBTech)** at checkout.
2. PrestaShop redirects to the HayBTech hosted payment page.
3. Customer pays via their preferred mobile money provider.
4. HayBTech sends a signed webhook -- the module verifies and updates order status.

---


---

## Security

- **HMAC-SHA256 Webhook Verification** with constant-time comparison
- **Zero External Dependencies** -- embedded SDK, no supply chain risk
- **Secret Masking** in logs and debug output
- **1 MB Payload Limit** to prevent DoS
- **CRLF Guard** against header injection

---

## Troubleshooting

| Issue                      | Solution                                                          |
|:---------------------------|:------------------------------------------------------------------|
| Module not appearing       | Clear cache, verify folder is named `haybtech`                    |
| Payment option not showing | Ensure module is active and assigned to customer groups            |
| Webhooks returning 403     | Verify webhook secret matches the HayBTech dashboard              |
| Orders not updating        | Check logs under **Advanced Parameters > Logs**                   |

---

MIT License
