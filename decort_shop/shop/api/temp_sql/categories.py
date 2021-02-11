static function loadCategory(){

        $sql = 'CREATE TEMPORARY TABLE t_category_buffer(
            `source_id` VARCHAR(100) NOT NULL ,
            `parent_source_id` VARCHAR(100) NOT NULL ,
            `name` VARCHAR(255) NULL ,
            `name_ukr` VARCHAR(255) NULL ,
            `name_en` VARCHAR(255) NULL ,
            PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('categories'));

        file_put_contents(Yii::getAlias('@runtime/download/categories.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/categories.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_category_buffer',
            [
                'source_id',
                'parent_source_id',
                'name',
                'name_ukr',
                'name_en',
            ],
            $batch
        )->execute();

        $sql = [
            "INSERT INTO {{%catalog_category}} (source_id)
                SELECT source_id FROM t_category_buffer
                WHERE source_id NOT IN (SELECT source_id FROM {{%catalog_category}} WHERE source_id IS NOT NULL)",

            'UPDATE {{%catalog_category}} c, {{%catalog_category}} p, t_category_buffer b
                SET c.parent_id = p.id
                WHERE c.source_id = b.source_id AND p.source_id = b.parent_source_id',

            "DELETE FROM {{%catalog_category}} WHERE source_id NOT IN (SELECT source_id FROM t_category_buffer)",

            "TRUNCATE TABLE {{%catalog_category_lang}}",

            "INSERT INTO {{%catalog_category_lang}} (name, lang_code, category_id)
            SELECT b.name, 'ru', c.id FROM t_category_buffer b, {{%catalog_category}} c
            WHERE b.source_id = c.source_id AND name <> ''",

            "INSERT INTO {{%catalog_category_lang}} (name, lang_code, category_id)
            SELECT b.name_ukr, 'uk', c.id FROM t_category_buffer b, {{%catalog_category}} c
            WHERE b.source_id = c.source_id AND trim(name_ukr) <> ''",

            "INSERT INTO {{%catalog_category_lang}} (name, lang_code, category_id)
            SELECT b.name_en, 'en', c.id FROM t_category_buffer b, {{%catalog_category}} c
            WHERE b.source_id = c.source_id AND trim(name_en) <> ''",
        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }