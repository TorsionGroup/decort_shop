static public function loadProduct(){


        $sql = 'CREATE TEMPORARY TABLE t_product_buffer (
            `source_id`             VARCHAR(100) NOT NULL,
            `category_source_id`    VARCHAR(100) NULL,
            `brand_source_id`       VARCHAR(100) NULL,
            `offer_source_id`       VARCHAR(100) NULL,
            `code`                  VARCHAR(200) NULL,
            `name`                  VARCHAR(200) NULL,
            `name_ukr`              VARCHAR(200) NULL,
            `name_en`               VARCHAR(200) NULL,
            `comment`               TEXT         NULL,
            `comment_ukr`           TEXT         NULL,
            `comment_en`            TEXT         NULL,
            `article`               VARCHAR(100) NULL,
            `specification`         VARCHAR(100) NULL,
            `ABC`                   VARCHAR(1)   NULL,
            `description`           TEXT         NULL,
            `price_category`        VARCHAR(100) NULL,
            `weight`                DECIMAL(15,3)NULL,
            `pack_qty`              INT(11)      NULL,
            `product_type`          INT(11)      NULL,
            `create_date`           DATETIME     NULL,
            `income_date`           DATETIME     NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('products'));

        file_put_contents(Yii::getAlias('@runtime/download/products.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/products.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_product_buffer',
                    [
                        'source_id',
                        'category_source_id',
                        'brand_source_id',
                        'offer_source_id',
                        'code',
                        'name',
                        'name_ukr',
                        'name_en',
                        'comment',
                        'comment_ukr',
                        'comment_en',
                        'article',
                        'specification',
                        'ABC',
                        'price_category',
                        'description',
                        'weight',
                        'pack_qty',
                        'product_type',
                        'create_date',
                        'income_date',
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_product_buffer',
            [
                'source_id',
                'category_source_id',
                'brand_source_id',
                'offer_source_id',
                'code',
                'name',
                'name_ukr',
                'name_en',
                'comment',
                'comment_ukr',
                'comment_en',
                'article',
                'specification',
                'ABC',
                'price_category',
                'description',
                'weight',
                'pack_qty',
                'product_type',
                'create_date',
                'income_date',
            ],
            $batch
        )->execute();

        $clearKey = 'b.article';
        foreach(Product::getUnSymbols() as $symbol){
            $symbol = Yii::$app->db->quoteSql($symbol);
            $clearKey = "REPLACE($clearKey,'$symbol', '')";
        }

        $_1cSourceType = self::_1C_SOURCE_TYPE;

        $sql = [
            "INSERT INTO {{%product}} (source_id, code, source_type)
            SELECT source_id, code, '$_1cSourceType' FROM t_product_buffer
            WHERE source_id NOT IN(SELECT source_id FROM {{%product}} WHERE source_id IS NOT NULL)",

            "DELETE FROM {{%product}} WHERE source_type = '$_1cSourceType' AND
                source_id NOT IN (SELECT source_id FROM t_product_buffer)",

            "UPDATE {{%product}} p, t_product_buffer b
              SET
                p.specification = b.specification,
                p.article       = b.article,
                p.create_date   = b.create_date,
                p.income_date   = b.income_date,
                p.search_key    = $clearKey,
                p.weight        = b.weight,
                p.ABC           = b.ABC,
                p.price_category= b.price_category,
                p.advanced_description = b.description,
                p.pack_qty      = b.pack_qty,
                p.product_type  = b.product_type,
                p.code          = TRIM(LEADING '0' FROM b.code),
                p.source_type   = '$_1cSourceType'
            WHERE p.source_id = b.source_id",

            "UPDATE {{%product}} p
              SET p.product_type  = 0
            WHERE p.source_id NOT IN (SELECT b.source_id FROM t_product_buffer b)",


            "UPDATE {{%product}} p, {{%product_lang}} l
                SET l.source_type = p.source_type
                WHERE l.product_id = p.id and p.source_type = '$_1cSourceType'",

            "DELETE FROM {{%product_lang}} WHERE source_type = '$_1cSourceType' ",

            "INSERT INTO {{%product_lang}} (product_id, name, comment, lang_code, source_type)
                SELECT id, name, CONCAT_WS('. ',`description`, `comment`), 'RU', '$_1cSourceType'
                 FROM {{%product}} p, t_product_buffer b
                 WHERE b.source_id = p.source_id",

            "INSERT INTO {{%product_lang}} (product_id, name, comment, lang_code, source_type)
                SELECT id, name_ukr, CONCAT_WS('. ', `description`, `comment_ukr`), 'UK', '$_1cSourceType'
                 FROM {{%product}} p, t_product_buffer b
                 WHERE b.source_id = p.source_id",

            "INSERT INTO {{%product_lang}} (product_id, name, comment, lang_code, source_type)
              SELECT id, name_en, CONCAT_WS('. ', `description`, `comment_en`), 'EN', '$_1cSourceType'
              FROM {{%product}} p, t_product_buffer b
              WHERE b.source_id = p.source_id",

            "UPDATE {{%product}} set brand_id = null, category_id = null, offer_id = null WHERE source_type = '$_1cSourceType'",

            'UPDATE {{%product}} p, {{%brand}} br, t_product_buffer b
                SET p.brand_id = br.id
              WHERE p.source_id = b.source_id AND br.source_id = b.brand_source_id',

            'UPDATE {{%product}} p, {{%catalog_category}} c, t_product_buffer b
                SET p.category_id = c.id
              WHERE p.source_id = b.source_id AND c.source_id = b.category_source_id',

            'UPDATE {{%product}} p, {{%offer}} o, t_product_buffer b
                SET p.offer_id = o.id
              WHERE p.source_id = b.source_id AND o.source_id = b.offer_source_id',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

        try{
            self::loadPrice();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');

        try{
            self::loadCross();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');

        try{
            self::loadProductApplicability();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');

        try{
            self::loadProductDescription();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }

        try{
            self::loadProductPriceCategory();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }

        self::getMethodEcho('text');
    }
