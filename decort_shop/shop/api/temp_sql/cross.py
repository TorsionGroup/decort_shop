static public function loadCross(){
        $sql = 'CREATE TEMPORARY TABLE t_cross_buffer (
            `product_source_id` VARCHAR(100) NOT NULL,
            `brand_name`        VARCHAR(100) NULL,
            `article_nr`        VARCHAR(100) NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('cross'));

        file_put_contents(Yii::getAlias('@runtime/download/cross.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/cross.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_cross_buffer',
                    [
                        'product_source_id',
                        'brand_name',
                        'article_nr',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_cross_buffer',
            [
                'product_source_id',
                'brand_name',
                'article_nr',
            ],
            $batch
        )->execute();

        $clearKey = 'b.article_nr';
        foreach(Product::getUnSymbols() as $symbol){
            $symbol = Yii::$app->db->quoteSql($symbol);
            $clearKey = "REPLACE($clearKey,'$symbol', '')";
        }

        $sql = [
            'TRUNCATE TABLE {{%cross}}',

            "INSERT INTO {{%cross}}(product_id,brand_name,article_nr,search_nr)
              SELECT DISTINCT p.id, b.brand_name, b.article_nr, $clearKey
                FROM t_cross_buffer b
                JOIN {{%product}} p ON p.source_id = b.product_source_id",
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }