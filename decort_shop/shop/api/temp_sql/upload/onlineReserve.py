static function onlineReserve($agreement_id, $user_id){
        date_default_timezone_set(Yii::$app->formatter->timeZone);
        /* @var $agreement CustomerAgreement */
        $agreement = CustomerAgreement::findOne($agreement_id);
        $data = [
            'agreement_source'  => $agreement->source_id,
            'deficit_available' => ArrayHelper::getValue($agreement->customer, 'deficit_available'),
            'items' => [],
        ];

        /* @var $item OrderItem */
        $items = OrderItem::find()->where([
            'order_id' => Order::find()->where([
                'agreement_id' => $agreement_id,
                'user_id' => $user_id,
                'status' => Order::RESERVE_STATUS,
            ])
                ->select('id')
                ->column()
        ])
            ->indexBy('product_id')
            ->all();

        foreach($items as $item){
            $updateDate = new \DateTime($item->update_date);
            if($updateDate->diff(new \DateTime())->h + $updateDate->diff(new \DateTime())->d * 24 > Order::RESERVE_LIVE){
                $item->delete();
            }else{
                $data['items'][] = [
                    'product_source' => ArrayHelper::getValue($item->product, 'source_id'),
                    'qty' => $item->qty,
                ];
            }
        }

        $params = new \SoapVar(["Data" => json_encode($data)], SOAP_ENC_OBJECT);

        $result =  self::getSoapClient()->SetReserve($params)->return;
        $data = json_decode($result, true);
        if(isset($data['Refresh'])){
            self::refreshStock($data['Refresh'], $agreement->customer->sale_policy);
        }

        if(isset($data['Reserve'])){
            $processedIds = [];
            foreach($data['Reserve'] as $row){
                /* @var $product Product */
                if($product = Product::findOne(['source_id' => $row['product_source']])){
                    $processedIds[] = $product->id;
                    if(isset($items[$product->id]) ){
                        $item = $items[$product->id];
                        if($item->qty != $row['qty']){
                            if(! $item->old_qty and $item->qty < $row['qty']){
                                $item->old_qty = $item->qty;
                            }
                            $item->qty = $row['qty'];
                            $item->save(false);
                        }
                    }else{
                        $item = new OrderItem();
                        $item->order_id = Order::getCart($agreement_id,null,Order::RESERVE_STATUS)->id;
                        $item->product_id = $product->id;
                        $item->price = $product->getAgreementPrice($agreement);
                        $item->currency_id = $agreement->currency_id;
                        $item->save(false);
                    }
                }
            }
            foreach($items as $item){
                if(! isset($processedIds[$item->product_id]) ){
                    $item->old_qty = $item->qty;
                    if(! $item->old_qty){
                        $item->old_qty = $item->qty;
                    }
                    $item->qty = 0;
                }
            }
        }
    }