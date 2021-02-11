static function dropShippingArgeement($agreement, $order, $sum){
        /* @var $agreement CustomerAgreement */
        /* @var $order Order */
        $data = json_encode([
            'agreement_source' => $agreement->source_id,
            'order_source' => $order->source,
            'sum' => $sum,
            'type' => 'agreement',
        ]);

        $params = new \SoapVar(["Data" => $data], SOAP_ENC_OBJECT);
        $result =  self::getSoapClient()->SetDropshippingTransfer($params)->return;

        file_put_contents(Yii::getAlias('@runtime/drp.txt'), $result);
        $result = file_get_contents(Yii::getAlias('@runtime/drp.txt'));
        $data = json_decode($result, true);

        if(ArrayHelper::getValue($data, 'Status') == 'Error'){
            return ArrayHelper::getValue($data, 'Reason');
        }

        if(ArrayHelper::getValue($data, 'Status') == 'OK'){
            $sql = 'CREATE TEMPORARY TABLE IF NOT EXISTS t_dropshipping_transfer_buffer (
            `credit` DECIMAL(15,2) NULL,
            `order_source` VARCHAR(100) NOT NULL,
            `dropshipping` INTEGER(11) NULL,
            `balance` DECIMAL(15,2) NULL,
            `currency_source` VARCHAR(100) NOT NULL,
            `agreement_source` VARCHAR(100) NOT NULL,
            `debit` DECIMAL(15,2) NULL,
            `customer_source` VARCHAR(100) NOT NULL
            );';
            Yii::$app->db->createCommand($sql)->execute();

            $batch = [];

            foreach($data['Refresh'] as $elem){
                $batch [] = $elem;
            }

            Yii::$app->db->createCommand()->batchInsert(
                't_dropshipping_transfer_buffer',
                [
                    'credit',
                    'order_source',
                    'dropshipping',
                    'balance',
                    'currency_source',
                    'agreement_source',
                    'debit',
                    'customer_source',
                ],
                $batch
            )->execute();

            $sql = [
                'DELETE FROM {{%balance}} WHERE customer_id IN
                       (SELECT DISTINCT c.id FROM t_dropshipping_transfer_buffer JOIN {{%customer}} c ON c.source_id=customer_source)',
                'DELETE FROM {{%dropshipping_wallet}} WHERE agreement_id IN
                       (SELECT DISTINCT a.id FROM t_dropshipping_transfer_buffer JOIN trs_customer_agreement a ON a.source_id=agreement_source)',
                'INSERT INTO {{%dropshipping_wallet}}(order_id, agreement_id, currency_id, debit, credit, balance)
                        SELECT o.id, ag.id, ag.currency_id, credit, debit, balance
                        FROM t_dropshipping_transfer_buffer
                            JOIN {{%order}} o ON o.source = order_source
                            JOIN {{%customer_agreement}} ag ON ag.source_id = agreement_source
                            WHERE dropshipping=1
                            ',
                'INSERT INTO {{%balance}}(customer_id, currency_id, balance, agreement_id)
                        SELECT ag.customer_id, ag.currency_id, SUM(balance) AS balance, ag.id
                        FROM t_dropshipping_transfer_buffer
                            JOIN {{%customer_agreement}} ag ON ag.source_id = agreement_source GROUP BY (ag.id)
                            ',
            ];

            $command = Yii::$app->db->createCommand();
            foreach($sql as $query){
                $command->setSql($query);
                $command->execute();
            }
        }

        return true;
    }