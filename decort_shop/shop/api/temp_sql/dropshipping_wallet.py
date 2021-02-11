static function loadDropshippingWallet(){
        $sql = 'CREATE TEMPORARY TABLE t_dropshipping_wallet_buffer (
            `agreement_source` VARCHAR(100) NOT NULL,
            `order_source` VARCHAR(100) NOT NULL,
            `credit` DECIMAL(15,2) NULL,
            `debit` DECIMAL(15,2) NULL,
            `balance` DECIMAL(15,2) NULL
            );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('dropshipping_wallet'));

        file_put_contents(Yii::getAlias('@runtime/download/dropshipping_wallet.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/dropshipping_wallet.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_dropshipping_wallet_buffer',
            [
                'agreement_source',
                'order_source',
                'credit',
                'debit',
                'balance',
            ],
            $batch
        )->execute();

        $sql = [
            'TRUNCATE TABLE {{%dropshipping_wallet}}',
            'INSERT INTO {{%dropshipping_wallet}}(order_id, agreement_id, currency_id, debit, credit, balance)
                        SELECT o.id, ag.id, ag.currency_id, debit, credit, balance
                        FROM t_dropshipping_wallet_buffer
                            JOIN {{%order}} o ON o.source = order_source
                            JOIN {{%customer_agreement}} ag ON ag.source_id = agreement_source
                            ',
        ];

        $command = Yii::$app->db->createCommand();
        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }
    }