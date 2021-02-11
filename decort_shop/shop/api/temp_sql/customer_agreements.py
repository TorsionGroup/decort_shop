static function loadCustomerAgreement(){
        $sql = 'CREATE TEMPORARY TABLE t_agreement_buffer(
            `source_id` VARCHAR(100) NOT NULL ,

            `customer_id` int(11) DEFAULT NULL ,
            `customer_source_id` VARCHAR(100) NOT NULL ,

            `currency_id` int(11) DEFAULT NULL  ,
            `currency_source_id` VARCHAR(200) NULL ,

            `price_type_id` int(11) DEFAULT NULL ,
            `price_type_source_id` VARCHAR(200) NULL ,

            `code` VARCHAR(45) NULL ,
            `name` VARCHAR(100) NULL ,
            `number` VARCHAR(45) NULL ,
            `discount` decimal(15,2) NULL ,
            `is_status` int(11) NULL ,
            `is_active` int(11) NULL ,
            PRIMARY KEY (`source_id`) );';

        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('customer_agreements'));

        file_put_contents(Yii::getAlias('@runtime/download/customer_agreements.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/customer_agreements.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_agreement_buffer',
            [
                'source_id',
                'customer_source_id',
                'currency_source_id',
                'price_type_source_id',
                'code',
                'name',
                'number',
                'discount',
                'is_status',
                'is_active',
            ],
            $batch
        )->execute();

        $sql = [
            'INSERT INTO {{%customer_agreement}} (source_id)
              SELECT source_id FROM t_agreement_buffer
              WHERE source_id NOT IN (SELECT source_id FROM {{%customer_agreement}} WHERE source_id IS NOT NULL)',

            'DELETE FROM {{%customer_agreement}} WHERE source_id NOT IN (SELECT source_id FROM t_agreement_buffer)',

            'UPDATE t_agreement_buffer b, {{%customer}} c
              SET b.customer_id = c.id
              WHERE b.customer_source_id = c.source_id',

            'UPDATE t_agreement_buffer b, {{%currency}} c
              SET b.currency_id = c.id
              WHERE b.currency_source_id = c.source_id',

            'UPDATE t_agreement_buffer b, {{%price_type}} c
              SET b.price_type_id = c.id
              WHERE b.price_type_source_id = c.source_id',

            "UPDATE {{%customer_agreement}} c, t_agreement_buffer b
              SET
                c.code          = b.code,
                c.name          = b.name,
                c.number        = b.number,
                c.discount      = b.discount,
                c.is_status     = b.is_status,
                c.is_active     = b.is_active,
                c.customer_id   = b.customer_id,
                c.currency_id   = b.currency_id,
                c.price_type_id = b.price_type_id
             WHERE c.source_id = b.source_id",

        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }
