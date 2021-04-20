import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/categories.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shop_catalogcategory',
                  columns=('source_id', 'parent_source', 'name_ru', 'name_uk', 'name_en', 'url', 'enabled', 'level',
                           'lft', 'rght', 'tree_id'), sep='|')
conn.commit()
print('Load Catalog Category')
