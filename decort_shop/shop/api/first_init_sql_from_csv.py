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
    'source_id', 'main_source_id', 'manager_source_id', 'code', 'name', 'sale_policy', 'city', 'region_id'), sep='|')
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
    cur.copy_from(file, 'shop_price_category_buffer', columns=('source_id', 'inner_name'), sep='|')
conn.commit()
print('Load Price Category')

conn.close()
print('Connection closed')
