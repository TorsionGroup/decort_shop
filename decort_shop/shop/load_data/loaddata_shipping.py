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

    def load_novaposhta_cities(self):
        novaposhta_cities = self.client.service.GetData('novaposhta_cities')
        data = base64.b64decode(novaposhta_cities)
        file = open('cache/novaposhta_cities.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_novaposhta_branches(self):
        novaposhta_branches = self.client.service.GetData('novaposhta_branches')
        data = base64.b64decode(novaposhta_branches)
        file = open('cache/novaposhta_branches.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_novaposhta_streetes(self):
        novaposhta_streetes = self.client.service.GetData('novaposhta_streetes')
        data = base64.b64decode(novaposhta_streetes)
        file = open('cache/novaposhta_streetes.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()


LoadDataShipping = LoadDataShipping()
LoadDataShipping.load_regions()
LoadDataShipping.load_novaposhta_regions()
LoadDataShipping.load_novaposhta_cities()
LoadDataShipping.load_novaposhta_branches()
LoadDataShipping.load_novaposhta_streetes()
print('Load Data Shipping')
