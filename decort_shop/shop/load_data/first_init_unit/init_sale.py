import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/sales.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'managers_sale',
                  columns=('product', 'customer', 'qty', 'date'), sep='|')
conn.commit()
print('Load Sale')

with open('../cache/sale_tasks.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'managers_saletask',
                  columns=('product', 'customer', 'qty'), sep='|')
conn.commit()
print('Load Sale Task')
