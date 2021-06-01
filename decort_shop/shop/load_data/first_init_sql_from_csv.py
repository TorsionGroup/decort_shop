import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('cache/product_manufacturer_model.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'products_productmanufacturermodel',
                  columns=('product', 'manufacturer_name', 'model_name', 'manufacturer_tecdoc_id',
                           'model_tecdoc_id'), sep='|')
conn.commit()
print('Load Product Manufacturer Model')

conn.close()
print('Connection closed')
