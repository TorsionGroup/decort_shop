import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/products.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_product',
                  columns=(
                      'source_id', 'category', 'brand', 'offer', 'code', 'name_ru', 'name_uk', 'name_en',
                      'comment_ru', 'comment_uk', 'comment_en', 'article', 'specification', 'abc', 'price_category',
                      'advanced_description', 'keywords_ru', 'keywords_uk', 'keywords_en', 'manufacturer_name',
                      'model_name', 'weight', 'pack_qty', 'product_type', 'create_date', 'income_date'), sep='|')
conn.commit()
print('Load Product')

with open('../cache/prices.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_price',
                  columns=('product', 'price_type', 'currency', 'price'), sep='|')
conn.commit()
print('Load Prices')

with open('../cache/stocks.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_stock',
                  columns=('product', 'stock_name', 'amount_total', 'amount_account'), sep='|')
conn.commit()
print('Load Stocks')

with open('../cache/deficit.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_deficitreserve',
                  columns=('product', 'sale_policy', 'amount'), sep='|')
conn.commit()
print('Load Deficit')

with open('../cache/description.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_productdescription',
                  columns=('product', 'property', 'value'), sep='|')
conn.commit()
print('Load Description')

with open('../cache/applicability.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_productapplicability',
                  columns=('product', 'vehicle', 'modification', 'engine', 'year'), sep='|')

conn.commit()
print('Load Applicability')

with open('../cache/cross.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_cross',
                  columns=('product', 'brand', 'article_nr'), sep='|')
conn.commit()
print('Load Cross')

with open('../cache/product_manufacturer_model.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_productmanufacturermodel',
                  columns=('product', 'manufacturer_name', 'model_name', 'manufacturer_tecdoc_id',
                           'model_tecdoc_id'), sep='|')
conn.commit()
print('Load Product Manufacturer Model')

