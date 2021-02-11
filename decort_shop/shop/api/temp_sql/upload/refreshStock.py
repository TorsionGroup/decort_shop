static function refreshStock($data, $salePolicy = null){
        $alreadyDeleted = [];

        foreach($data as $row){
            if($product = Product::findOne(['source_id' => $row['product_source']])){

                if(! in_array($product->id, $alreadyDeleted)){

                    Stock::deleteAll(['product_id' => $product->id]);

                    DeficitReserve::deleteAll(['product_id' => $product->id, 'sale_policy' => $salePolicy]);


                    $alreadyDeleted[] = $product->id;
                }

                if( (int)$row['amount_total'] > 0 ){
                    $stock = new Stock();
                    $stock->product_id = $product->id;
                    $stock->stock_name = $row['stock_name'];
                    $stock->amount_total = $row['amount_total'];
                    $stock->amount_account = $row['amount_account'];
                    $stock->save(false);

                    if($row['deficit_reserve'] and $salePolicy){
                        $deficit = new DeficitReserve();
                        $deficit->product_id = $product->id;
                        $deficit->sale_policy = $salePolicy;
                        $deficit->amount = $row['deficit_reserve'];
                        $deficit->save(false);
                    }
                }
            }
        }
    }