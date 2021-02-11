static function uploadOrder(){
        /* @var $model Order */
        $data = [];
        foreach(Order::find()->where(['status' => Order::PREPARED_STATUS])->all() as $model){
            $data[] = $model->json;
        }

        $params = new \SoapVar(["Data" => json_encode($data)], SOAP_ENC_OBJECT);

        $result =  json_decode(self::getSoapClient()->SetOrder($params)->return, true);

        if(isset($result['orders'])){
            foreach($result['orders'] as $id => $source){
                if($model = Order::findOne($id)){
                    $model->source = $source;
                    $model->status = Order::POSTED_STATUS;
                    foreach($model->orderItem as $item){
                        $item->source = $model->source.$item->product->source_id;
                        $item->save(false);
                        if($item->product){
                            // Чистим лист ожидания, вдруг есть по заказанным итемам
                            if($waitList = $item->product->getUserWaitList($model->user_id)->one() ){
                                $waitList->delete();
                            }
                        }
                    }
                    $model->save(false);
                }
            }
        }

        if(isset($result['brand']) ){
            foreach($result['brand'] as $key => $value){
                /* @var $brand Brand */
                if($brand = Brand::findOne($key)){
                    $brand->source_id = $value;
                    $brand->source_type = self::_1C_SOURCE_TYPE;
                    $brand->save(false);
                }
            }
        }

        if(isset($result['product']) ){
            foreach($result['product'] as $key => $value){
                /* @var $product Product */
                if($product = Product::findOne($key)){
                    $product->source_id = $value;
                    $product->source_type = self::_1C_SOURCE_TYPE;
                    $product->save(false);
                }
            }
        }
    }