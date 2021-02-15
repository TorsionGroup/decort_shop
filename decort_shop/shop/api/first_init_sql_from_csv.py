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
    cur.copy_from(file, 'shop_product',
                  columns=(
                      'source_id', 'category_id', 'brand_id', 'offer_id', 'code', 'name', 'name_ukr', 'name_en',
                      'comment', 'comment_ukr', 'comment_en', 'article', 'specification', 'ABC', 'price_category',
                      'advanced_description', 'weight', 'pack_qty', 'product_type', 'create_date',
                      'income_date'), sep='|')
conn.commit()
print('Load Product')

with open('cache/customer_points.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_customerpoint', columns=('customer_source_id', 'source_id', 'name', 'add'), sep='|')
conn.commit()
print('Load Customer Point')

with open('cache/customer_agreements.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_customeragreement',
                  columns=('source_id', 'customer_source_id', 'currency_source_id', 'price_type_source_id',
                           'code', 'name', 'number', 'discount', 'is_status', 'is_active'), sep='|')
conn.commit()
print('Load Customer Agreement')

with open('cache/balances.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_balance',
                  columns=('customer_source', 'agreement_source', 'currency_source', 'balance', 'past_due'), sep='|')
conn.commit()
print('Load Balance')

with open('cache/customer_discounts.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_customerdiscount_buffer',
                  columns=('criteria_source_id', 'customer_source_id', 'agreement_source_id',
                           'price_type_source_id', 'criteria_type', 'discount'), sep='|')
conn.commit()
print('Load Customer Discount')

with open('cache/dropshipping_wallet.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_dropshippingwallet',
                  columns=('agreement_source', 'order_source', 'credit', 'debit', 'balance'), sep='|')
conn.commit()
print('Load Dropshipping Wallet')

with open('cache/prices.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_price',
                  columns=('product_source_id', 'price_type_source_id', 'currency_source_id', 'price'), sep='|')
conn.commit()
print('Load Price')


conn.close()
print('Connection closed')
