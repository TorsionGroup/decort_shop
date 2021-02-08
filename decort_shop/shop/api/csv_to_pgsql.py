import csv
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

t_sql = '''CREATE TEMPORARY TABLE shop_currency_buffer (
    code character varying(250),
    name character varying(250),
    title character varying(250),
    source_id character varying(300),
    rate numeric(15,5),
    mult integer );'''

cur.execute(t_sql)
conn.commit()

with open('download/currencies.csv', 'r+', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_currency_buffer', columns=('source_id', 'code', 'name', 'title', 'rate', 'mult'), sep='|')
conn.commit()



conn.close()
print('Connection closed')
