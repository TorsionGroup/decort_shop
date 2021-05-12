import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/customer_discounts.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customerdiscount',
                  columns=('source_id', 'brand', 'customer', 'agreement',
                           'price_type', 'criteria_type', 'discount'), sep='|')
conn.commit()
print('Load Customer Discount')

with open('../cache/customer_contacts.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customercontact',
                  columns=('source', 'source_customer', 'name', 'email', 'phone', 'is_user', 'birthday'), sep='|')
conn.commit()
print('Load Customer Contact')

with open('../cache/customer_points.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customerpoint', columns=('customer', 'source_id', 'name', 'add'), sep='|')
conn.commit()
print('Load Customer Point')

with open('../cache/customer_agreements.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_customeragreement',
                  columns=('source_id', 'customer', 'currency', 'price_type',
                           'code', 'name', 'number', 'discount', 'is_status', 'is_active'), sep='|')
conn.commit()
print('Load Customer Agreement')

with open('../cache/balances.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'customers_balance',
                  columns=('customer', 'agreement', 'currency', 'balance', 'past_due'), sep='|')
conn.commit()
print('Load Balance')
