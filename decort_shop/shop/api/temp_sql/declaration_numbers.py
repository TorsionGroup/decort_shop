static function loadDeclarationNumber(){

        $sql = 'CREATE TEMPORARY TABLE t_declaration_number_buffer (
            `order_source`    VARCHAR(100) NOT NULL,
            `declaration_number` VARCHAR(100) NOT NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('declaration_numbers'));

        file_put_contents(Yii::getAlias('@runtime/download/declaration_number.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/declaration_number.csv'), 'r');

        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);

            if(count($batch) == 1000){
                Yii::$app->db->createCommand()->batchInsert(
                    't_declaration_number_buffer',
                    [
                        'order_source',
                        'declaration_number'
                    ],
                    $batch
                )->execute();
                $batch = [];
            }
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_declaration_number_buffer',
            [
                'order_source',
                'declaration_number'
            ],
            $batch
        )->execute();

        $sql = "UPDATE {{%order}} o, t_declaration_number_buffer b SET o.declaration_number = b.declaration_number WHERE o.source = b.order_source";
        Yii::$app->db->createCommand($sql)->execute();

    }