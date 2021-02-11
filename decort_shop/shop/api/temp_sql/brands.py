static function loadBrand(){
        $sql = 'CREATE TEMPORARY TABLE t_brand_buffer (`source_id` VARCHAR(100) NOT NULL ,  `name` VARCHAR(45) NULL ,  PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('brands'));

        file_put_contents(Yii::getAlias('@runtime/download/brands.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/brands.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_brand_buffer',
            [
                'source_id',
                'name',
            ],
            $batch
        )->execute();

        $_1cSourceType = self::_1C_SOURCE_TYPE;

        $sql = [
            "INSERT INTO {{%brand}}(name, source_id, source_type)
                SELECT name, source_id, '$_1cSourceType' FROM t_brand_buffer
                WHERE source_id NOT IN (select source_id from {{%brand}} WHERE source_id IS NOT NULL AND source_type = '$_1cSourceType')",

            "UPDATE {{%brand}} br, t_brand_buffer bf
                SET br.name = bf.name
                WHERE br.source_id = bf.source_id AND br.source_type = '$_1cSourceType'",

            "DELETE FROM {{%brand}}
                WHERE source_id NOT IN (
                    SELECT source_id FROM t_brand_buffer
                ) AND source_type = '$_1cSourceType'",

        ];


        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }


    }