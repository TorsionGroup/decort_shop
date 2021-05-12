import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/orders.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'orders_order',
                  columns=('order_source', 'agreement', 'order_number', 'waybill_number',
                           'comment', 'source_type', 'has_precept', 'has_waybill', 'order_date'), sep='|')
conn.commit()
print('Load Orders')

with open('../cache/order_items.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'orders_orderitem',
                  columns=('order_source', 'product_source', 'currency_source', 'quantity', 'price', 'reserved',
                           'executed'), sep='|')
conn.commit()
print('Load Orders Items')
