static function dropShippingCard($order, $sum, $card){
        /* @var $agreement CustomerAgreement */
        /* @var $order Order */
        $data = json_encode([
            'order_source' => $order->source,
            'sum' => $sum,
            'type' => 'cart',
            'cart' => $card
        ]);

        $params = new \SoapVar(["Data" => $data], SOAP_ENC_OBJECT);
        $result =  self::getSoapClient()->SetDropshippingTransfer($params)->return;

        return true;
    }