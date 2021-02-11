static public function loadStock(){

        $sql = 'CREATE TEMPORARY TABLE t_stock_buffer (
            `product_source_id` VARCHAR(100) NOT NULL,
            `stock_name`        VARCHAR(255) NULL,
            `amount_total`      INT NULL,
            `amount_account`    INT NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('stocks'));

        file_put_contents(Yii::getAlias('@runtime/download/stocks.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/stocks.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_stock_buffer',
                    [
                        'product_source_id',
                        'stock_name',
                        'amount_total',
                        'amount_account',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_stock_buffer',
            [
                'product_source_id',
                'stock_name',
                'amount_total',
                'amount_account',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%stock}}',

            "INSERT INTO {{%stock}}(product_id, stock_name, amount_total, amount_account)
              SELECT DISTINCT p.id, b.stock_name, b.amount_total, b.amount_account
                FROM t_stock_buffer b
                JOIN {{%product}} p ON p.source_id = b.product_source_id",

            'UPDATE {{%product}} SET is_active = 0, is_exists = 0',

            'UPDATE {{%product}} p, {{%stock}}
              SET is_active = 1, is_exists = 1
              WHERE p.id = product_id AND amount_total > 0',

            'UPDATE {{%product}} p, {{%brand}} b
              SET is_active = 1
              WHERE p.brand_id = b.id AND b.wait_list = 1',

            'UPDATE {{%wait_list}} SET is_active = 0',

            'UPDATE {{%wait_list}} p, {{%stock}} s
              SET is_active = 1
              WHERE p.product_id = s.product_id AND amount_total > 0',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

        WaitList::sendAlert();

        self::loadDeficit();
    }