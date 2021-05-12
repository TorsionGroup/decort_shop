import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/dropshipping_wallet.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'dropshipping_dropshippingwallet',
                  columns=('agreement', 'order_order', 'credit', 'debit', 'balance'), sep='|')
conn.commit()
print('Load Dropshipping Wallet')
