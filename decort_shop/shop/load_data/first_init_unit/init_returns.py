import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/returns.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'returns_proformreturn',
                  columns=('source', 'source_customer', 'source_agreement', 'source_order', 'comment'), sep='|')
conn.commit()
print('Load Returns')

