static function onlineOrder($model){

        /* @var $product Product */
        foreach($model->orderItem as $item){
            $item->old_price = 0;
            $item->old_qty = 0;
            $item->save(false);
        }


        if($model->status == $model::RESERVE_STATUS){
            $model->status = $model::CART_STATUS;
            $model->save();
        }

        self::onlineReserve($model->agreement_id, $model->user_id);

        $data = $model->json;

        $params = new \SoapVar(["Data" => json_encode($data)], SOAP_ENC_OBJECT);
        $result =  self::getSoapClient()->SetOnlineOrder($params)->return;
        $data = json_decode($result, true);


        if(isset($data['Refresh'])){
            self::refreshStock($data['Refresh'], $model->customer->sale_policy);
        }

        $model->source = ArrayHelper::getValue($data, 'Source');
        $model->import_status = ArrayHelper::getValue($data, 'Status');
        $model->import_reason = ArrayHelper::getValue($data, 'Reason');
        $model->save(false);

        if($data['Status'] == 'OK'){
            $model->status = Order::POSTED_STATUS;
            $model->save(false);

            $orderItem = ArrayHelper::index($model->orderItem, 'product_id');

            foreach($data['Items'] as $row){
                /* @var $item OrderItem */
                if($product = Product::findOne(['source_id' => $row['product_source']]) and $item = $orderItem[$product->id]){

                    $item->old_qty  = null;
                    $item->old_price= null;

                    $item->qty      = $row['order_qty'];
                    $item->price    = $row['price'];
                    $item->reserved = $row['reserve_qty'];
                    $item->save();
                }
            }


        }elseif($data['Status'] == 'Fail'){

            $model->status = Order::UNCHECKED_STATUS;
            $model->save(false);
            // send mail to admin
            $model->getMailWithUncheckedStatus();

        }else{
            if(isset($data['Items'])){

                $orderItem = ArrayHelper::index($model->orderItem, 'product_id');
                foreach($data['Items'] as $row){
                    /* @var $item OrderItem */
                    if($product = Product::findOne(['source_id' => $row['product_source']]) and $item = $orderItem[$product->id]){
                        $item->old_qty = $item->qty;
                        $item->old_price = $item->price;
                        $item->qty  = $row['qty_response'];
                        $item->price= $row['price_response'];
                        $item->save();
                    }
                }
            }
            return false;
        }

        return true;

    }