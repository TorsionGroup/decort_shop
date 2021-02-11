static function loadProductApplicability(){
        $sql = 'CREATE TEMPORARY TABLE t_product_applicability_buffer (
            `product_source_id` VARCHAR(100) NOT NULL,
            `vehicle`        VARCHAR(200) NULL,
            `modification`   VARCHAR(200) NULL,
            `engine`   VARCHAR(200) NULL,
            `year`   VARCHAR(200) NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('applicability'));

        file_put_contents(Yii::getAlias('@runtime/download/applicability.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/applicability.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_product_applicability_buffer',
                    [
                        'product_source_id',
                        'vehicle',
                        'modification',
                        'engine',
                        'year'
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }
        if($batch){
            Yii::$app->db->createCommand()->batchInsert(
                't_product_applicability_buffer',
                [
                    'product_source_id',
                    'vehicle',
                    'modification',
                    'engine',
                    'year'
                ],
                $batch
            )->execute();
        }

        $sql = [
            'TRUNCATE TABLE {{%product_applicability}}',

            "INSERT INTO {{%product_applicability}}(product_id,vehicle,modification, engine, `year`)
              SELECT DISTINCT p.id, vehicle,modification, engine, `year`
                FROM t_product_applicability_buffer b
                JOIN {{%product}} p ON p.source_id = b.product_source_id",
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }