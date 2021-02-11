static function uploadRequest(){
        /* @var $model UserRequest */
        $data = [];
        foreach(UserRequest::find()->where('source_id IS NULL')->all() as $model){
            $data[] = $model->json;
        }

        $params = new \SoapVar(["Data" => json_encode($data)], SOAP_ENC_OBJECT);
        $result =  self::getSoapClient()->SetRequest($params)->return;

        foreach(json_decode($result, true) as $id => $source){
            if($model = UserRequest::findOne($id)){
                $model->source_id = $source;
                $model->save(false);
            }
        }
    }