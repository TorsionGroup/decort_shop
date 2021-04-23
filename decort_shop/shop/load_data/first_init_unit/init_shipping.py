import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/regions.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shipping_region',
                  columns=('source', 'name'), sep='|')
conn.commit()
print('Load Regions')

with open('../cache/novaposhta_regions.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shipping_novaposhtaregion',
                  columns=('source', 'name'), sep='|')
conn.commit()
print('Load Nova Poshta Regions')

with open('../cache/novaposhta_cities.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shipping_novaposhtacity',
                  columns=('source', 'source_region', 'name'), sep='|')
conn.commit()
print('Load Nova Poshta City')

with open('../cache/novaposhta_branches.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shipping_novaposhtabranche',
                  columns=('source', 'source_city', 'name', 'branche_type', 'max_weight_place', 'max_weight'), sep='|')
conn.commit()
print('Load Nova Poshta Branches')

with open('../cache/novaposhta_streetes.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'shipping_novaposhtastreet',
                  columns=('source', 'source_city', 'name', 'street_type'), sep='|')
conn.commit()
print('Load Nova Poshta Street')

