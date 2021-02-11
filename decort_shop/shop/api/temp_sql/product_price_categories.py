static function loadProductPriceCategory(){

        $sql = 'CREATE TEMPORARY TABLE t_product_price_category_buffer (`product_source_id` VARCHAR(100) NOT NULL ,  `price_category_source_id` VARCHAR(100) NOT NULL  );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('product_price_categories'));

        file_put_contents(Yii::getAlias('@runtime/download/product_price_categories.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/product_price_categories.csv'), 'r');
        $batch = [];

        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_product_price_category_buffer',
            [
                'product_source_id',
                'price_category_source_id',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%product_price_category}}',

            'INSERT INTO {{%product_price_category}} (product_id, price_category_id)
            SELECT DISTINCT pr.id, pc.id FROM t_product_price_category_buffer b
            JOIN {{%product}} pr ON pr.source_id = b.product_source_id
            JOIN {{%price_category}} pc ON pc.source_id = b.price_category_source_id',
        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }