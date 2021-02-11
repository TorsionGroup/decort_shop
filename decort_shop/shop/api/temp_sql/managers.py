static function loadManager(){
        $sql = 'CREATE TEMPORARY TABLE t_manager_buffer(
            `source_id` VARCHAR(100) NOT NULL ,
            `name` VARCHAR(100) NULL ,
            PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('managers'));

        file_put_contents(Yii::getAlias('@runtime/download/managers.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/managers.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_manager_buffer',
            [
                'source_id',
                'name',
            ],
            $batch
        )->execute();

        $sql = "INSERT INTO {{%manager}} (source_id)
            SELECT source_id FROM t_manager_buffer
            WHERE source_id NOT IN (SELECT source_id FROM {{%manager}} WHERE source_id IS NOT NULL)";
        Yii::$app->db->createCommand($sql)->execute();

        $sql = 'UPDATE {{%manager}} m, t_manager_buffer b
            SET m.inner_name = b.name
            WHERE m.source_id = b.source_id';
        Yii::$app->db->createCommand($sql)->execute();

    }