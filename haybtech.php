<?php
/**
 * Plugin Name: HayBTech for PrestaShop
 * Author: HayBTech Team
 * Version: 1.0.0
 */

if (!defined('_PS_VERSION_')) {
    exit;
}

class HayBTech extends PaymentModule
{
    public function __construct()
    {
        $this->name = 'haybtech';
        $this->tab = 'payments_gateways';
        $this->version = '1.0.0';
        $this->author = 'HayBTech Team';
        $this->need_instance = 1;

        parent::__construct();

        $this->displayName = $this->l('HayBTech');
        $this->description = $this->l('Acceptez Orange Money, Wave et Free Money sur votre boutique.');
        
        // Load SDK
        require_once _PS_MODULE_DIR_ . $this->name . '/lib/sdk/HayBTech.php';
        require_once _PS_MODULE_DIR_ . $this->name . '/lib/sdk/HayBTechClient.php';
    }

    public function install()
    {
        return parent::install() &&
            $this->registerHook('paymentOptions') &&
            $this->registerHook('paymentReturn') &&
            Configuration::updateValue('HAYBTECH_TEST_MODE', 1);
    }

    public function getContent()
    {
        $output = '';

        // Admin configuration form logic
        if (Tools::isSubmit('btnSubmit')) {
            $secretKey = (string) Tools::getValue('HAYBTECH_SECRET_KEY');
            
            if (!empty($secretKey) && !str_starts_with($secretKey, 'sk_')) {
                $output .= $this->displayError($this->l('Clé secrète invalide. Elle doit commencer par "sk_".'));
            } else {
                Configuration::updateValue('HAYBTECH_SECRET_KEY', $secretKey);
                Configuration::updateValue('HAYBTECH_WEBHOOK_SECRET', Tools::getValue('HAYBTECH_WEBHOOK_SECRET'));
                $output .= $this->displayConfirmation($this->l('Réglages mis à jour.'));
            }
        }

        return $output . $this->displayForm();
    }

    public function hookPaymentOptions($params)
    {
        if (!$this->active) return;

        $newOption = new PrestaShop\PrestaShop\Core\Payment\PaymentOption();
        $newOption->setModuleName($this->name)
                  ->setCallToActionText($this->l('Payer par Mobile Money (HayBTech)'))
                  ->setAction($this->context->link->getModuleLink($this->name, 'validation', [], true));

        return [$newOption];
    }
}
