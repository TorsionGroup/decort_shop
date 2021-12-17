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
        self.client = Client('http://192.168.75.104/live/ws/decort?wsdl', transport=transport, settings=settings)

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
            name character varying(300),
            center character varying(300),
            area_ref character varying(300),
            center_ref character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_regions.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtaregion_buffer',
                          columns=('name', 'center', 'area_ref', 'center_ref'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO shipping_novaposhtaregion (area_ref)
                 SELECT area_ref FROM shipping_novaposhtaregion_buffer
                 WHERE area_ref NOT IN (SELECT area_ref FROM shipping_novaposhtaregion WHERE area_ref IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtaregion r
            SET
                name = b.name,
                center = b.center,
                center_ref = b.center_ref       
            FROM shipping_novaposhtaregion_buffer b
            WHERE r.area_ref = b.area_ref;'''
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
            name character varying(300),
            name_ru character varying(300),
            region character varying(300),
            city_ref character varying(300),
            area_ref character varying(300),
            city_id character varying(300),
            settlement_type character varying(300),
            settlement_type_description_ru character varying(300),
            settlement_type_description character varying(300),
            np_region character varying(300),
            regions_description character varying(300),
            regions_description_ru character varying(300),
            index1 character varying(300),
            index2 character varying(300),
            index_coatsu1 character varying(300),
            np_latitude character varying(300),
            np_longitude character varying(300)  );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_cities.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtacity_buffer',
                          columns=('name', 'name_ru', 'region', 'city_ref', 'area_ref', 'city_id', 'settlement_type',
                                   'settlement_type_description_ru', 'settlement_type_description', 'np_region',
                                   'regions_description', 'regions_description_ru', 'index1', 'index2', 'index_coatsu1',
                                   'np_latitude', 'np_longitude'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO shipping_novaposhtacity (city_ref)
                         SELECT city_ref FROM shipping_novaposhtacity_buffer
                         WHERE city_ref NOT IN (SELECT city_ref FROM shipping_novaposhtacity WHERE city_ref IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM shipping_novaposhtacity
                        WHERE city_ref NOT IN (SELECT city_ref FROM shipping_novaposhtacity);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtacity c
            SET
                name = b.name,
                name_ru = b.name_ru,
                region = b.region,
                city_ref = b.city_ref,
                area_ref = b.area_ref,
                city_id = b.city_id,
                settlement_type = b.settlement_type,
                settlement_type_description_ru = b.settlement_type_description_ru,
                settlement_type_description = b.settlement_type_description,
                np_region = b.np_region,
                regions_description = b.regions_description,
                regions_description_ru = b.regions_description_ru,
                index1 = b.index1,
                index2 = b.index2,
                index_coatsu1 = b.index_coatsu1,
                np_latitude = b.np_latitude,
                np_longitude = b.np_longitude                      
            FROM shipping_novaposhtacity_buffer b
            WHERE c.city_ref = b.city_ref;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shipping_novaposhtacity c
            SET region_id_id = r.id                               
            FROM shipping_novaposhtaregion r
            WHERE c.area_ref = r.area_ref;'''
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
            name character varying(300),
            name_ru character varying(300),
            branche_type character varying(300),
            city character varying(300),
            number integer,
            max_weight_place integer,
            max_weight integer,
            wh_ref character varying(300),
            wh_type_ref character varying(300),
            city_ref character varying(300),
            latitude character varying(300),
            longitude character varying(300)      );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_branches.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtabranche_buffer',
                          columns=('name', 'name_ru', 'branche_type', 'city', 'number', 'max_weight_place', 'max_weight',
                                   'wh_ref', 'wh_type_ref', 'city_ref', 'latitude', 'longitude'),
                          sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO shipping_novaposhtabranche (wh_ref)
                        SELECT wh_ref FROM shipping_novaposhtabranche_buffer
                        WHERE wh_ref NOT IN (SELECT wh_ref FROM shipping_novaposhtabranche WHERE wh_ref IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtabranche c
            SET
                name = b.name,
                name_ru = b.name_ru,
                branche_type = b.branche_type,
                city = b.city,
                number = b.number,
                max_weight_place = b.max_weight_place,
                max_weight = b.max_weight,
                wh_ref = b.wh_ref,
                wh_type_ref = b.wh_type_ref,
                city_ref = b.city_ref,
                latitude = b.latitude,
                longitude = b.longitude       
            FROM shipping_novaposhtabranche_buffer b
            WHERE c.wh_ref = b.wh_ref;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shipping_novaposhtabranche b
            SET city_id_id = c.id                               
            FROM shipping_novaposhtacity c
            WHERE b.city_ref = c.city_ref;'''
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
            name character varying(300),
            street_type character varying(300),
            city character varying(300),
            street_type_ref character varying(300),
            street_ref character varying(300),
            city_ref character varying(300)   );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/novaposhta_streetes.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shipping_novaposhtastreet_buffer',
                          columns=('name', 'street_type', 'city', 'street_type_ref', 'street_ref', 'city_ref'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO shipping_novaposhtastreet (street_ref)
                        SELECT street_ref FROM shipping_novaposhtastreet_buffer
                        WHERE street_ref NOT IN (SELECT street_ref FROM shipping_novaposhtastreet WHERE street_ref IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shipping_novaposhtastreet c
            SET
                name = b.name,
                street_type = b.street_type,                
                city = b.city,
                street_type_ref = b.street_type_ref,                   
                city_ref = b.city_ref       
            FROM shipping_novaposhtastreet_buffer b
            WHERE c.street_ref = b.street_ref;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shipping_novaposhtastreet s
            SET city_id_id = c.id                               
            FROM shipping_novaposhtacity c
            WHERE s.city_ref = c.city_ref;'''
        cur.execute(upd_sql)
        self.conn.commit()


LoadDataShipping = LoadDataShipping()
LoadDataShipping.load_regions()
LoadDataShipping.load_novaposhta_regions()
LoadDataShipping.load_novaposhta_cities()
LoadDataShipping.load_novaposhta_branches()
LoadDataShipping.load_novaposhta_streetes()
print('Load Data Shipping')
