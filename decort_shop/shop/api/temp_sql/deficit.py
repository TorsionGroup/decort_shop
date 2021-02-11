static function loadDeficit(){

        $sql = 'CREATE TEMPORARY TABLE t_deficit_buffer (
            `product_source_id` VARCHAR(100) NOT NULL,
            `sale_policy`       VARCHAR(100) NULL,
            `amount`            INT NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('deficit'));

        file_put_contents(Yii::getAlias('@runtime/download/deficit.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/deficit.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_deficit_buffer',
                    [
                        'product_source_id',
                        'sale_policy',
                        'amount',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_deficit_buffer',
            [
                'product_source_id',
                'sale_policy',
                'amount',
            ],
            $batch
        )->execute();

        $sql = [

            'TRUNCATE TABLE {{%deficit_reserve}}',

            'INSERT INTO {{%deficit_reserve}} (product_id, sale_policy, amount)
                SELECT id, sale_policy, amount FROM t_deficit_buffer JOIN {{%product}} ON product_source_id = source_id',

            'UPDATE {{%product}}, {{%deficit_reserve}} SET is_active = 1 WHERE id = product_id AND is_active = 0',

        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }