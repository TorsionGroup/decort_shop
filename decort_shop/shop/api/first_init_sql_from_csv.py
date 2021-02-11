import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('cache/managers.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_manager', columns=('source_id', 'name'), sep='|')
conn.commit()
print('Load Managers')

with open('cache/currencies.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_currency', columns=('source_id', 'code', 'name', 'title', 'rate', 'mult'), sep='|')
conn.commit()
print('Load Currencies')

with open('cache/customers.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_customer', columns=(
        'source_id', 'main_source_id', 'manager_source_id', 'code', 'name', 'sale_policy', 'city', 'region_id'),
                  sep='|')
conn.commit()
print('Load Customers')

with open('cache/brands.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_brand', columns=('source_id', 'name'), sep='|')
conn.commit()
print('Load Brands')

with open('cache/price_types.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_price_type', columns=('source_id', 'name'), sep='|')
conn.commit()
print('Load Price Types')

with open('cache/price_categories.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_price_category', columns=('source_id', 'inner_name'), sep='|')
conn.commit()
print('Load Price Category')

with open('cache/categories.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_catalogcategory',
                  columns=('source_id', 'parent_id', 'name', 'name_ukr', 'name_en'), sep='|')
conn.commit()
print('Load Catalog Category')

with open('cache/offers.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_offer',
                  columns=('source_id', 'name', 'group', 'title'), sep='|')
conn.commit()
print('Load Offer')

with open('cache/products.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_product_buffer',
                  columns=(
                      'source_id', 'category_id', 'brand_id', 'offer_id', 'code', 'name', 'name_ukr', 'name_en',
                      'comment', 'comment_ukr', 'comment_en', 'article', 'specification', 'ABC', 'price_category',
                      'advanced_description', 'weight', 'pack_qty', 'product_type', 'create_date',
                      'income_date'), sep='|')
conn.commit()
print('Load Product')

conn.close()
print('Connection closed')
