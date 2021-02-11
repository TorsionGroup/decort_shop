static function loadBalance(){
        $sql = 'CREATE TEMPORARY TABLE t_balance_buffer (
            `customer_source` VARCHAR(100) NOT NULL,
            `agreement_source` VARCHAR(100) NOT NULL,
            `currency_source` VARCHAR(100) NOT NULL,
            `balance` DECIMAL(15,2) NULL,
            `past_due` DECIMAL(15,2) NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('balances'));

        file_put_contents(Yii::getAlias('@runtime/download/balances.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/balances.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_balance_buffer',
            [
                'customer_source',
                'agreement_source',
                'currency_source',
                'balance',
                'past_due',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%balance}}',
            'INSERT INTO {{%balance}}(customer_id, agreement_id, currency_id, balance, past_due)
                        SELECT cust.id, ag.id, cur.id, balance, past_due
                        FROM t_balance_buffer
                            JOIN {{%customer}} cust ON cust.source_id = customer_source
                            JOIN {{%currency}} cur ON cur.source_id = currency_source
                            JOIN {{%customer_agreement}} ag ON ag.source_id = agreement_source
                            ',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

    }