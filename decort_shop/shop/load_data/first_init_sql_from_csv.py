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
    cur.copy_from(file, 'shop_manager', columns=('source_id', 'inner_name', 'is_active'), sep='|')
conn.commit()
print('Load Managers')

with open('cache/currencies.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_currency', columns=('source_id', 'code', 'name', 'title', 'rate', 'mult'), sep='|')
conn.commit()
print('Load Currencies')

with open('cache/customers.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_customer', columns=(
        'source_id', 'main_customer', 'manager', 'code', 'name', 'sale_policy', 'city', 'region_id'),
                  sep='|')
conn.commit()
print('Load Customers')

with open('cache/price_types.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_pricetype', columns=('source_id', 'name'), sep='|')
conn.commit()
print('Load Price Types')

with open('cache/brands.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_brand', columns=('source_id', 'name', 'supplier_id', 'is_recommended'), sep='|')
conn.commit()
print('Load Brands')

with open('cache/price_categories.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_pricecategory', columns=('source_id', 'inner_name'), sep='|')
conn.commit()
print('Load Price Category')

with open('cache/categories.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_catalogcategory',
                  columns=('source_id', 'parent_source', 'name_ru', 'name_uk', 'name_en', 'url', 'enabled', 'level',
                           'lft', 'rght', 'tree_id'), sep='|')
conn.commit()
print('Load Catalog Category')

with open('cache/offers.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_offer', columns=('source_id', 'name', 'group_name', 'title'), sep='|')
conn.commit()
print('Load Offer')

with open('cache/products.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_product',
                  columns=(
                      'source_id', 'category', 'brand', 'offer', 'code', 'name_ru', 'name_uk', 'name_en',
                      'comment_ru', 'comment_uk', 'comment_en', 'article', 'specification', 'abc', 'price_category',
                      'advanced_description', 'keywords_ru', 'keywords_uk', 'keywords_en', 'weight', 'pack_qty',
                      'product_type', 'create_date', 'income_date'), sep='|')
conn.commit()
print('Load Product')

with open('cache/customer_points.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customerpoint', columns=('customer', 'source_id', 'name', 'add'), sep='|')
conn.commit()
print('Load Customer Point')

with open('cache/customer_agreements.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customeragreement',
                  columns=('source_id', 'customer', 'currency', 'price_type',
                           'code', 'name', 'number', 'discount', 'is_status', 'is_active'), sep='|')
conn.commit()
print('Load Customer Agreement')

with open('cache/balances.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_balance',
                  columns=('customer', 'agreement', 'currency', 'balance', 'past_due'), sep='|')
conn.commit()
print('Load Balance')

with open('cache/customer_discounts.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customerdiscount',
                  columns=('source_id', 'brand', 'customer', 'agreement',
                           'price_type', 'criteria_type', 'discount'), sep='|')
conn.commit()
print('Load Customer Discount')

with open('cache/customer_contacts.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customercontact',
                  columns=('source', 'source_customer', 'name', 'email', 'is_user', 'birthday'), sep='|')
conn.commit()
print('Load Customer Contact')

with open('cache/dropshipping_wallet.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'dropshipping_dropshippingwallet',
                  columns=('agreement', 'order_order', 'credit', 'debit', 'balance'), sep='|')
conn.commit()
print('Load Dropshipping Wallet')

with open('cache/prices.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_price',
                  columns=('product', 'price_type', 'currency', 'price'), sep='|')
conn.commit()
print('Load Price')

with open('cache/sales.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'managers_sale',
                  columns=('product', 'customer', 'qty', 'date'), sep='|')
conn.commit()
print('Load Sale')

with open('cache/sale_tasks.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'managers_saletask',
                  columns=('product', 'customer', 'qty'), sep='|')
conn.commit()
print('Load Sale Task')

with open('cache/stocks.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_stock',
                  columns=('product', 'stock_name', 'amount_total', 'amount_account'), sep='|')
conn.commit()
print('Load Stock')

with open('cache/deficit.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_deficitreserve',
                  columns=('product', 'sale_policy', 'amount'), sep='|')
conn.commit()
print('Load Deficit Reserve')

with open('cache/description.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_productdescription',
                  columns=('product', 'property', 'value'), sep='|')
conn.commit()
print('Load Product Description')

with open('cache/applicability.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_productapplicability',
                  columns=('product', 'vehicle', 'modification', 'engine', 'year'), sep='|')
conn.commit()
print('Load Product Applicability')

with open('cache/cross.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_cross',
                  columns=('product', 'brand', 'article_nr'), sep='|')
conn.commit()
print('Load Cross')

with open('cache/orders.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'orders_order',
                  columns=('order_source', 'agreement', 'order_number', 'waybill_number',
                           'comment', 'source_type', 'has_precept', 'has_waybill', 'order_date'), sep='|')
conn.commit()
print('Load Order')

with open('cache/order_items.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'orders_orderitem',
                  columns=('order_source', 'product_source', 'currency_source', 'quantity', 'price', 'reserved',
                           'executed'), sep='|')
conn.commit()
print('Load Order Item')

with open('cache/regions.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shipping_region', columns=('source', 'name'), sep='|')
conn.commit()
print('Load Shipping Regions')

with open('../cache/returns.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'returns_proformreturn',
                  columns=('source', 'source_customer', 'source_agreement', 'source_order', 'comment'), sep='|')
conn.commit()
print('Load Returns')


conn.close()
print('Connection closed')
