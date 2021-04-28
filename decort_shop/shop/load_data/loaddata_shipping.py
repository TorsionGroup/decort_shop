import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataShipping:
    def __init__(self):
        session = Session()
        session.auth = HTTPBasicAuth('Robot', 'Robot')
        transport = Transport(session=session, timeout=600)
        settings = Settings(xml_huge_tree=True)
        self.client = Client('http://192.168.75.115:8005/live/ws/decort?wsdl', transport=transport, settings=settings)

        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="decort_shop",
            user="torsion_prog",
            password="sdr%7ujK")

    def load_regions(self):
        regions = self.client.service.GetData('regions')
        data = base64.b64decode(regions)
        file = open('cache/regions.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shipping_region_buffer (
            source character varying(300),
            name character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/regions.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_region_buffer', columns=('source', 'name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shipping_region r
            SET
                name = b.name       
            FROM shipping_region_buffer b
            WHERE r.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_novaposhta_regions(self):
        novaposhta_regions = self.client.service.GetData('novaposhta_regions')
        data = base64.b64decode(novaposhta_regions)
        file = open('cache/novaposhta_regions.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shipping_novaposhtaregion_buffer (
            source character varying(300),
            name character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_regions.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtaregion_buffer',
                          columns=('source', 'name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtaregion r
            SET
                name = b.name       
            FROM shipping_novaposhtaregion_buffer b
            WHERE r.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_novaposhta_cities(self):
        novaposhta_cities = self.client.service.GetData('novaposhta_cities')
        data = base64.b64decode(novaposhta_cities)
        file = open('cache/novaposhta_cities.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shipping_novaposhtacity_buffer (
            source character varying(300),
            source_region character varying(300),
            name character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_cities.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtacity_buffer',
                          columns=('source', 'source_region', 'name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtacity c
            SET
                source_region = b.source_region,
                name = b.name       
            FROM shipping_novaposhtacity_buffer b
            WHERE c.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shipping_novaposhtacity c
            SET region_id = r.id                               
            FROM shipping_novaposhtaregion r
            WHERE c.source_region = r.source;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_novaposhta_branches(self):
        novaposhta_branches = self.client.service.GetData('novaposhta_branches')
        data = base64.b64decode(novaposhta_branches)
        file = open('cache/novaposhta_branches.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shipping_novaposhtabranche_buffer (
            source character varying(300),
            source_city character varying(300),
            name character varying(300),
            branche_type character varying(300),
            max_weight_place integer,
            max_weight integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_branches.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtabranche_buffer',
                          columns=('source', 'source_city', 'name', 'branche_type', 'max_weight_place', 'max_weight'),
                          sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtabranche c
            SET
                source_city = b.source_city,
                name = b.name,
                branche_type = b.branche_type,
                max_weight_place = b.max_weight_place,
                max_weight = b.max_weight       
            FROM shipping_novaposhtabranche_buffer b
            WHERE c.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shipping_novaposhtabranche b
            SET city_id = c.id                               
            FROM shipping_novaposhtacity c
            WHERE b.source_city = c.source;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_novaposhta_streetes(self):
        novaposhta_streetes = self.client.service.GetData('novaposhta_streetes')
        data = base64.b64decode(novaposhta_streetes)
        file = open('cache/novaposhta_streetes.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shipping_novaposhtastreet_buffer (
            source character varying(300),
            source_city character varying(300),
            name character varying(300),
            street_type character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_streetes.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtastreet_buffer',
                          columns=('source', 'source_city', 'name', 'street_type'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtastreet c
            SET
                source_city = b.source_city,
                name = b.name,
                street_type = b.street_type       
            FROM shipping_novaposhtastreet_buffer b
            WHERE c.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shipping_novaposhtastreet s
            SET city_id = c.id                               
            FROM shipping_novaposhtacity c
            WHERE s.source_city = c.source;'''
        cur.execute(upd_sql)
        self.conn.commit()


LoadDataShipping = LoadDataShipping()
LoadDataShipping.load_regions()
LoadDataShipping.load_novaposhta_regions()
LoadDataShipping.load_novaposhta_cities()
LoadDataShipping.load_novaposhta_branches()
LoadDataShipping.load_novaposhta_streetes()
print('Load Data Shipping')
