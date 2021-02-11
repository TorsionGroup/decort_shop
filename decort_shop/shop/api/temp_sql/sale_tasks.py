static function loadSaleTasks(){
        $sql = 'CREATE TEMPORARY TABLE t_sale_tasks_buffer (
            `product_source` VARCHAR(100) NOT NULL,
            `customer_source` VARCHAR(100) NOT NULL,
            `qty` INTEGER NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('sale_tasks'));

        file_put_contents(Yii::getAlias('@runtime/download/sale_tasks.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/sale_tasks.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_sale_tasks_buffer',
            [
                'product_source',
                'customer_source',
                'qty',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%sale_task}}',
            'INSERT INTO {{%sale_task}}(product_id, customer_id, qty)
                        SELECT p.id, c.id, qty
                        FROM t_sale_tasks_buffer
                            JOIN {{%product}} p ON p.source_id = product_source
                            JOIN {{%customer}} c ON c.source_id = customer_source
                            ',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }