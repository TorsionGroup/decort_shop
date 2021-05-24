import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="decort_shop",
    user="torsion_prog",
    password="sdr%7ujK"
)
cur = conn.cursor()

with open('../cache/tecdoc_manufacturer.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'tecdoc_manufacturer',
                  columns=('source', 'name', 'manufacturer_tecdoc_id', 'country', 'canbedisplayed', 'ispassengercar',
                           'iscommercialvehicle', 'ismotorbike', 'isengine', 'isaxle'), sep='|')
conn.commit()
print('Load Tecdoc Manufacturer')

with open('../cache/tecdoc_manufacturer_model.csv', 'r', encoding='utf-8') as file:
    cur.copy_from(file, 'tecdoc_manufacturermodel',
                  columns=('source', 'source_manufacturer', 'name', 'constructioninterval', 'model_tecdoc_id',
                           'manufacturer_tecdoc_id', 'canbedisplayed', 'ispassengercar', 'iscommercialvehicle',
                           'ismotorbike', 'isengine', 'isaxle', 'commercial'), sep='|')
conn.commit()
print('Load Tecdoc Manufacturer Model')
