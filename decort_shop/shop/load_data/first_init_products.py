import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('cache/products.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_product',
                  columns=(
                      'source_id', 'category', 'brand', 'offer', 'code', 'name_ru', 'name_uk', 'name_en',
                      'comment_ru', 'comment_uk', 'comment_en', 'article', 'specification', 'abc', 'price_category',
                      'advanced_description', 'keywords_ru', 'keywords_uk', 'keywords_en', 'weight', 'pack_qty',
                      'product_type', 'create_date', 'income_date'), sep='|')
conn.commit()
print('Load Product')