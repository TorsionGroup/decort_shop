static function loadCustomerDiscount(){
        $sql = 'CREATE TEMPORARY TABLE t_discount_buffer (
            `criteria_source_id`    VARCHAR(100) NOT NULL,
            `customer_source_id`    VARCHAR(100) NULL,
            `agreement_source_id`   VARCHAR(100) NULL,
            `price_type_source_id`  VARCHAR(100) NULL,
            `criteria_type`         VARCHAR(100) NULL,
            `discount`              decimal(15,2) NULL);';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('customer_discounts'));

        file_put_contents(Yii::getAlias('@runtime/download/customer_discounts.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/customer_discounts.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_discount_buffer',
            [
                'criteria_source_id',
                'customer_source_id',
                'agreement_source_id',
                'price_type_source_id',
                'criteria_type',
                'discount',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%customer_discount}}',

            "INSERT INTO {{%customer_discount}}
                (customer_id, agreement_id, criteria_id, criteria_type, discount, price_type_id)
                SELECT a.customer_id, a.id, b.id, bf.criteria_type, bf.discount, pt.id
                FROM t_discount_buffer bf
                JOIN {{%customer_agreement}} a ON bf.agreement_source_id = a.source_id
                JOIN {{%brand}} b ON bf.criteria_source_id = b.source_id
                LEFT JOIN {{%price_type}} pt ON pt.source_id = bf.price_type_source_id",

            "INSERT INTO {{%customer_discount}}
                (customer_id, agreement_id, criteria_id, criteria_type, discount, price_type_id)
                SELECT a.customer_id, a.id, b.id, bf.criteria_type, bf.discount, pt.id
                FROM t_discount_buffer bf
                JOIN {{%customer_agreement}} a ON bf.agreement_source_id = a.source_id
                JOIN {{%offer}} b ON bf.criteria_source_id = b.source_id
                LEFT JOIN {{%price_type}} pt ON pt.source_id = bf.price_type_source_id",
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }