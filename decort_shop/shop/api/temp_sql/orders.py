static function loadOrder(){
        $sql = 'CREATE TEMPORARY TABLE t_order_buffer (
            `order_source`    VARCHAR(100) NOT NULL,
            `agreement_source_id` VARCHAR(100) NOT NULL,
            `order_number`    VARCHAR(100) NULL,
            `waybill_number`  VARCHAR(100) NULL,
            `comment`         VARCHAR(500) NULL,
            `source_type`     VARCHAR(100) NULL,
            `has_precept`     INT NULL,
            `has_waybill`     INT NULL,
            `order_date`      DATETIME
            );';
        Yii::$app->db->createCommand($sql)->execute();


        $data = base64_decode(self::getData('orders'));


        file_put_contents(Yii::getAlias('@runtime/download/orders.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/orders.csv'), 'r');

        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_order_buffer',
                    [
                        'order_source',
                        'agreement_source_id',
                        'order_number',
                        'waybill_number',
                        'comment',
                        'source_type',
                        'has_precept',
                        'has_waybill',
                        'order_date'
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_order_buffer',
            [
                'order_source',
                'agreement_source_id',
                'order_number',
                'waybill_number',
                'comment',
                'source_type',
                'has_precept',
                'has_waybill',
                'order_date'
            ],
            $batch
        )->execute();

        $sql = [
            'INSERT INTO {{%order}} (
                `agreement_id`,
                `status`,
                `delivery_method`,
                `create_date`,
                `update_date`,
                `comment`,
                `source`
            )
            SELECT DISTINCT a.id, '.Order::POSTED_STATUS.',\''.Order::OTHER.'\', order_date, order_date, comment, order_source
            FROM t_order_buffer b
            JOIN {{%customer_agreement}} a ON a.source_id = b.agreement_source_id
            WHERE order_source NOT IN (SELECT source FROM {{%order}} WHERE source IS NOT NULL)',

            'UPDATE {{%order}} o, t_order_buffer b SET
              status = CASE
                WHEN has_waybill THEN '.Order::WAYBILL_STATUS.'
                WHEN has_precept THEN '.Order::PRECEPT_STATUS.'
                ELSE status
                END,
                o.order_number = b.order_number,
                o.waybill_number = b.waybill_number,
                o.source_type = b.source_type
            WHERE o.source = b.order_source',

            'UPDATE {{%order}} o, t_order_buffer b, {{%customer_agreement}} a SET
              o.agreement_id = a.id
            WHERE o.source = b.order_source AND a.source_id = b.agreement_source_id',

        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }


        self::loadOrderItems();
        self::loadDeclarationNumber();

    }