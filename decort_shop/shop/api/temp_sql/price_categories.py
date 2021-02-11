static function loadPriceCategory(){

        $sql = 'CREATE TEMPORARY TABLE t_price_category_buffer
        (`source_id` VARCHAR(100) NOT NULL ,  `inner_name` VARCHAR(45) NULL ,  PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('price_categories'));

        file_put_contents(Yii::getAlias('@runtime/download/price_categories.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/price_categories.csv'), 'r');
        $batch = [];

        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_price_category_buffer',
            [
                'source_id',
                'inner_name',
            ],
            $batch
        )->execute();

        $sql = [
            'INSERT INTO {{%price_category}}(inner_name, source_id)
            SELECT inner_name, source_id FROM t_price_category_buffer
            WHERE source_id NOT IN (select source_id from {{%price_category}} WHERE source_id IS NOT NULL)',

            'UPDATE {{%price_category}} br, t_price_category_buffer bf
                SET br.inner_name = bf.inner_name
             WHERE br.source_id = bf.source_id',

            'DELETE FROM {{%price_category}} WHERE source_id NOT IN (SELECT source_id FROM t_price_category_buffer)',
        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }