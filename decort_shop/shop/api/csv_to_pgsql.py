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


class SqlData:

    def sql_brands(self):
        with open('download/brands.csv', 'r') as file:
            cur.copy_from(file, 'shop_brand', columns=('source_id', 'name'), sep='(|)')

    conn.commit()


sql = SqlData()
sql.sql_brands()
