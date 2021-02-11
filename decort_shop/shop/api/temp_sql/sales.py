static function loadSales(){
        $sql = 'CREATE TEMPORARY TABLE t_sales_buffer (
            `product_source` VARCHAR(100) NOT NULL,
            `customer_source` VARCHAR(100) NOT NULL,
            `qty` INTEGER NULL,
            `date` DATETIME
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('sales'));

        file_put_contents(Yii::getAlias('@runtime/download/sales.csv'), $data);

        $f = fopen(Yii::getAlias('@runtime/download/sales.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_sales_buffer',
            [
                'product_source',
                'customer_source',
                'qty',
                'date'
            ],
            $batch
        )->execute();

        $sql = [
            'DELETE FROM {{%sale}} WHERE `date` >= DATE_ADD(LAST_DAY(DATE_SUB(NOW(), INTERVAL 2 MONTH)), INTERVAL 1 DAY)',
            'INSERT INTO {{%sale}}(product_id, customer_id, qty, date)
                        SELECT p.id, c.id, qty, date
                        FROM t_sales_buffer
                            JOIN {{%product}} p ON p.source_id = product_source
                            JOIN {{%customer}} c ON c.source_id = customer_source
                        WHERE `date` >= DATE_ADD(LAST_DAY(DATE_SUB(NOW(), INTERVAL 2 MONTH)), INTERVAL 1 DAY)
                            ',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }