static function loadProductDescription(){

        $sql = 'CREATE TEMPORARY TABLE t_product_description_buffer (
            `product_source_id` VARCHAR(100) NOT NULL,
            `property`        VARCHAR(100) NULL,
            `value`        text NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('description'));

        file_put_contents(Yii::getAlias('@runtime/download/description.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/description.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_product_description_buffer',
                    [
                        'product_source_id',
                        'property',
                        'value',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }
        if($batch){
            Yii::$app->db->createCommand()->batchInsert(
                't_product_description_buffer',
                [
                    'product_source_id',
                    'property',
                    'value',
                ],
                $batch
            )->execute();
        }

        $sql = [
            'TRUNCATE TABLE {{%product_description}}',

            "INSERT INTO {{%product_description}}(product_id,property,value)
              SELECT DISTINCT p.id, property, value
                FROM t_product_description_buffer b
                JOIN {{%product}} p ON p.source_id = b.product_source_id",
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }


    }