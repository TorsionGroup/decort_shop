static function loadOffer(){
        $sql = 'CREATE TEMPORARY TABLE t_offer_buffer (
            `source_id` VARCHAR(100) NOT NULL,
            `name` VARCHAR(100) NULL,
            `group` VARCHAR(100) NULL,
            `title` VARCHAR(100) NULL,
            PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('offers'));

        file_put_contents(Yii::getAlias('@runtime/download/offers.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/offers.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_offer_buffer',
            [
                'source_id',
                'name',
                'group',
                'title',
            ],
            $batch
        )->execute();

        $sql = 'INSERT INTO {{%offer}}(name, source_id)
            SELECT name, source_id FROM t_offer_buffer
            WHERE source_id NOT IN (select source_id from {{%offer}} WHERE source_id IS NOT NULL)';
        Yii::$app->db->createCommand($sql)->execute();
        $sql = 'UPDATE {{%offer}} o, t_offer_buffer b
            SET
            o.name  = b.name,
            o.group = b.group,
            o.title = b.title
            WHERE o.source_id = b.source_id';
        Yii::$app->db->createCommand($sql)->execute();
    }