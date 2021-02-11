static function loadCustomer(){

        $sql = 'CREATE TEMPORARY TABLE t_customer_buffer(
            `source_id` VARCHAR(1000) NOT NULL ,
            `main_source_id` VARCHAR(100) NOT NULL ,
            `manager_source_id` VARCHAR(100) NOT NULL ,
            `code` VARCHAR(45) NULL ,
            `name` VARCHAR(1000) NULL ,
            `sale_policy` VARCHAR(200) NULL ,
            `city` VARCHAR(1000) NULL ,
            `region` VARCHAR(1000) NULL ,
            PRIMARY KEY (`source_id`) );';
        Yii::$app->db->createCommand($sql)->execute();

        $data = base64_decode(self::getData('customers'));

        file_put_contents(Yii::getAlias('@runtime/download/customers.csv'), $data);
        $f = fopen(Yii::getAlias('@runtime/download/customers.csv'), 'r');
        $batch = [];
        while($row = trim(fgets($f))){
            $batch[] = explode('(|)', $row);
        }

        Yii::$app->db->createCommand()->batchInsert(
            't_customer_buffer',
            [
                'source_id',
                'main_source_id',
                'manager_source_id',
                'code',
                'name',
                'sale_policy',
                'city',
                'region',
            ],
            $batch
        )->execute();

        $sql = [
            "INSERT INTO {{%customer}} (source_id)
            SELECT source_id FROM t_customer_buffer
            WHERE source_id NOT IN (SELECT source_id FROM {{%customer}} WHERE source_id IS NOT NULL)",

            "INSERT INTO {{%region}} (name)
              SELECT DISTINCT region FROM t_customer_buffer
              WHERE IFNULL(region, '') <> '' AND region NOT IN (SELECT name FROM {{%region}})",

            "DELETE FROM {{%region}} WHERE name NOT IN (SELECT DISTINCT region FROM t_customer_buffer)",

            "INSERT INTO {{%scenario_policy}} ({{%scenario_policy}}.sale_policy)
            SELECT DISTINCT t_customer_buffer.sale_policy FROM t_customer_buffer
            WHERE IFNULL(t_customer_buffer.sale_policy, '') <> '' AND t_customer_buffer.sale_policy NOT IN (SELECT {{%scenario_policy}}.sale_policy FROM {{%scenario_policy}})",

            "DELETE FROM {{%scenario_policy}} WHERE {{%scenario_policy}}.sale_policy NOT IN (SELECT DISTINCT t_customer_buffer.sale_policy FROM t_customer_buffer)",

            "UPDATE {{%customer}} c, {{%scenario_policy}} s, t_customer_buffer b SET
              c.deficit_available = s.deficit_available
              WHERE c.source_id = b.source_id AND s.sale_policy = b.sale_policy AND b.source_id NOT IN (SELECT * FROM (SELECT source_id FROM {{%customer}}) AS cus)",

            "UPDATE {{%customer}} c, {{%scenario_policy}} s, t_customer_buffer b SET
              c.online_reserve = s.online_reserve
              WHERE c.source_id = b.source_id AND s.sale_policy = b.sale_policy
              AND b.source_id NOT IN (SELECT * FROM (SELECT source_id FROM {{%customer}}) AS cus)",

            "UPDATE {{%customer}} c, {{%scenario_policy}} s, t_customer_buffer b SET
              c.online_order = s.online_order
              WHERE c.source_id = b.source_id AND s.sale_policy = b.sale_policy AND b.source_id NOT IN (SELECT * FROM (SELECT source_id FROM {{%customer}}) AS cus)",

            "UPDATE {{%customer}} c, t_customer_buffer b  SET
                 c.code        = b.code,
                 c.name        = b.name,
                 c.sale_policy = b.sale_policy,
                 c.city        = b.region
             WHERE c.source_id = b.source_id",

            "UPDATE {{%customer}} c, t_customer_buffer b, {{%customer}} main SET
                c.main_customer_id = main.id
               WHERE c.source_id = b.source_id AND main.source_id = b.main_source_id AND b.source_id <> b.main_source_id",

            "UPDATE {{%customer}} c, t_customer_buffer b, {{%manager}} m SET
                c.manager_id = m.id
               WHERE c.source_id = b.source_id AND m.source_id = b.manager_source_id",

            "UPDATE {{%customer}} c, {{%region}} r, t_customer_buffer b SET
              c.region_id = r.id
              WHERE c.source_id = b.source_id AND r.name = b.region",
        ];

        $command = Yii::$app->db->createCommand();

        foreach($sql as $query){
            $command->setSql($query);
            $command->execute();
        }

        try{
            self::loadCustomerPoint();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');

        try{
            self::loadCustomerAgreement();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');

        try{
            self::loadCustomerDiscount();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');

        try{
            self::loadBalance();
        }
        catch(\Exception $e) {
            echo $e->getMessage();
        }
        self::getMethodEcho('text');
    }