static function loadOrderItems(){
        $sql = 'CREATE TEMPORARY TABLE t_order_item_buffer (
            `order_source`      VARCHAR(100) NOT NULL,
            `product_source_id` VARCHAR(100) NOT NULL,
            `currency_source_id`VARCHAR(100) NOT NULL,
            `qty`               INT NULL,
            `reserved`          INT NULL,
            `executed`          INT NULL,
            `order_id`          INT NULL,
            `product_id`        INT NULL,
            `price`  DECIMAL(15,2) NULL,
            `key`VARCHAR(200),
            index (`key`)
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('order_items'));

        file_put_contents(Yii::getAlias('@runtime/download/order_items.csv'), $data);

        $f = fopen(Yii::getAlias('@runtime/download/order_items.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_order_item_buffer',
                    [
                        'order_source',
                        'product_source_id',
                        'currency_source_id',
                        'qty',
                        'price',
                        'reserved',
                        'executed',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_order_item_buffer',
            [
                'order_source',
                'product_source_id',
                'currency_source_id',
                'qty',
                'price',
                'reserved',
                'executed',
            ],
            $batch
        )->execute();

        $status = [
            Order::CART_STATUS,
            Order::PREPARED_STATUS,
            Order::WAITING_STATUS,
            Order::PURCHASE_STATUS,
           // Order::UNCHECKED_STATUS,
            Order::RESERVE_STATUS
        ];

        $sql = [
            'UPDATE t_order_item_buffer b, {{%order}} o, {{%product}} p SET
                b.`key` = concat(order_source,product_source_id),
                b.`order_id` = o.id,
                b.`product_id` = p.id
            WHERE b.order_source = o.source AND b.product_source_id = p.source_id',

            "CREATE TEMPORARY TABLE t_oi AS SELECT * FROM {{%order_item}} WHERE order_id IN (SELECT id FROM {{%order}} WHERE status IN(".implode(',', $status).") )",

            "TRUNCATE TABLE {{%order_item}}",

            'INSERT INTO {{%order_item}} (order_id, product_id, qty, price, reserved, executed, source, currency_id )
              SELECT order_id, product_id, qty, price, reserved, executed, source, currency_id FROM t_oi',

            'INSERT INTO {{%order_item}} (order_id, product_id, qty, price, reserved, executed, source, currency_id )
                SELECT order_id, product_id, qty, price, reserved, executed, `key`, c.id
                FROM t_order_item_buffer b
                JOIN {{%currency}} c ON b.currency_source_id = c.source_id
                WHERE b.order_id IS NOT NULL',

            'DELETE FROM trs_order where id not in (select order_id from trs_order_item) and status > 0 AND create_date  > (now() - INTERVAL 2 month);'
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }