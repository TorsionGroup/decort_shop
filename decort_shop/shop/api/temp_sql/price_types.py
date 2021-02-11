static function loadPriceType(){
        $sql = 'CREATE TEMPORARY TABLE t_pryce_type_buffer (`source_id` VARCHAR(100) NOT NULL ,  `name` VARCHAR(45) NULL ,  PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('price_types'));

        file_put_contents(Yii::getAlias('@runtime/download/price_types.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/price_types.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_pryce_type_buffer',
            [
                'source_id',
                'name',
            ],
            $batch
        )->execute();

        $sql = [
            'INSERT INTO {{%price_type}}(name, source_id)
            SELECT name, source_id FROM t_pryce_type_buffer
            WHERE source_id NOT IN (select source_id from {{%price_type}} WHERE source_id IS NOT NULL)',

            'UPDATE {{%price_type}} br, t_pryce_type_buffer bf SET br.name = bf.name WHERE br.source_id = bf.source_id',
        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }
