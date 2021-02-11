static private function loadCustomerPoint(){

        $sql = 'CREATE TEMPORARY TABLE t_point_buffer(
            `customer_source_id` VARCHAR(100) NOT NULL ,
            `source_id` VARCHAR(200) NOT NULL ,
            `name` VARCHAR(200) NULL ,
            `add` VARCHAR(200) NULL ,
            INDEX (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('customer_points'));

        file_put_contents(Yii::getAlias('@runtime/download/customer_points.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/customer_points.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_point_buffer',
            [
                'customer_source_id',
                'source_id',
                'name',
                'add',
            ],
            $batch
        )->execute();

        $sql = [

            'INSERT INTO {{%customer_point}} (source_id, customer_id, name)
              SELECT concat(source_id,customer_source_id) , 0, name FROM t_point_buffer
              WHERE concat(source_id,customer_source_id) NOT IN (SELECT source_id FROM {{%customer_point}} WHERE source_id IS NOT NULL)',

            "DELETE FROM {{%customer_point}} WHERE source_id NOT IN (SELECT concat(source_id,customer_source_id) FROM t_point_buffer)",

            'UPDATE t_point_buffer b, {{%customer_point}} p, {{%customer}} c
              SET
                p.customer_id = c.id,
                p.name = b.name
              WHERE b.customer_source_id = c.source_id AND concat(b.source_id, b.customer_source_id) = p.source_id',
        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }



    }