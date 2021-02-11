static public function loadPrice(){
        $sql = [
            'DROP TABLE IF EXISTS t_price_buffer',

            'CREATE TEMPORARY TABLE t_price_buffer (
            `product_source_id`     VARCHAR(100) NOT NULL,
            `price_type_source_id`  VARCHAR(100) NULL,
            `currency_source_id`    VARCHAR(100) NULL,
            `price`                 DECIMAL(15,2)     NULL
            );'
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

        $data = base64_decode(self::getData('prices'));

        file_put_contents(Yii::getAlias('@runtime/download/prices.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/prices.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_price_buffer',
                    [
                        'product_source_id',
                        'price_type_source_id',
                        'currency_source_id',
                        'price',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_price_buffer',
            [
                'product_source_id',
                'price_type_source_id',
                'currency_source_id',
                'price',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%price}}',

            'INSERT INTO {{%price}} (product_id, price_type_id, currency_id, price)
            SELECT p.id, prt.id, c.id, b.price
            FROM t_price_buffer b
            JOIN {{%product}} p ON p.source_id = b.product_source_id
            JOIN {{%price_type}} prt ON prt.source_id = b.price_type_source_id
            JOIN {{%currency}} c ON c.source_id = b.currency_source_id',

            'UPDATE {{%product}} p, {{%price}} pr, {{%currency}} c
                SET sort_price = price * rate / mult
              WHERE price_type_id = '.PriceType::BASE_PRICE_ID.' and currency_id = c.id AND p.id = pr.product_id',

            'UPDATE {{%product}} SET sort_price = 999999 WHERE sort_price IS NULL',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }