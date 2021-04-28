import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataTecdoc:
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

    def load_tecdoc_manufacturer(self):
        tecdoc_manufacturer = self.client.service.GetData('tecdoc_manufacturer')
        data = base64.b64decode(tecdoc_manufacturer)
        file = open('cache/tecdoc_manufacturer.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE tecdoc_manufacturer_buffer (
                source character varying(300),
                name character varying(300), 
                manufacturer_tecdoc_id character varying(300),
                canbedisplayed boolean,
                ispassengercar boolean,
                iscommercialvehicle boolean,
                ismotorbike boolean,
                isengine boolean,
                isaxle boolean );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/tecdoc_manufacturer.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'tecdoc_manufacturer_buffer',
                          columns=('source', 'name', 'manufacturer_tecdoc_id', 'canbedisplayed', 'ispassengercar',
                                   'iscommercialvehicle', 'ismotorbike', 'isengine', 'isaxle'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE tecdoc_manufacturer t
                SET
                    name = b.name,
                    manufacturer_tecdoc_id = b.manufacturer_tecdoc_id, 
                    canbedisplayed = b.canbedisplayed,
                    ispassengercar = b.ispassengercar,
                    iscommercialvehicle = b.iscommercialvehicle,
                    ismotorbike = b.ismotorbike,
                    isengine = b.isengine,                    
                    isaxle = b.isaxle            
                FROM tecdoc_manufacturer_buffer b
                WHERE t.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_tecdoc_manufacturer_model(self):
        tecdoc_manufacturer_model = self.client.service.GetData('tecdoc_manufacturer_model')
        data = base64.b64decode(tecdoc_manufacturer_model)
        file = open('cache/tecdoc_manufacturer_model.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE tecdoc_manufacturermodel_buffer (
                source character varying(300),
                source_manufacturer character varying(300),
                name character varying(300),
                constructioninterval character varying(300), 
                model_tecdoc_id character varying(300),  
                manufacturer_tecdoc_id character varying(300),
                canbedisplayed boolean,
                ispassengercar boolean,
                iscommercialvehicle boolean,
                ismotorbike boolean,
                isengine boolean,
                isaxle boolean );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/tecdoc_manufacturer_model.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'tecdoc_manufacturermodel_buffer',
                          columns=('source', 'source_manufacturer', 'name', 'constructioninterval', 'model_tecdoc_id',
                                   'manufacturer_tecdoc_id', 'canbedisplayed', 'ispassengercar', 'iscommercialvehicle',
                                   'ismotorbike', 'isengine', 'isaxle'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE tecdoc_manufacturermodel t
                SET
                    source_manufacturer = b.source_manufacturer,
                    name = b.name,
                    constructioninterval = b.constructioninterval,
                    model_tecdoc_id = b.model_tecdoc_id,
                    manufacturer_tecdoc_id = b.manufacturer_tecdoc_id, 
                    canbedisplayed = b.canbedisplayed,
                    ispassengercar = b.ispassengercar,
                    iscommercialvehicle = b.iscommercialvehicle,
                    ismotorbike = b.ismotorbike,
                    isengine = b.isengine,                    
                    isaxle = b.isaxle            
                FROM tecdoc_manufacturermodel_buffer b
                WHERE t.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE tecdoc_manufacturermodel t
            SET manufacturer_id = m.id                               
            FROM tecdoc_manufacturer m
            WHERE t.source_manufacturer = m.source;'''
        cur.execute(upd_sql)
        self.conn.commit()


LoadDataTecdoc = LoadDataTecdoc()
LoadDataTecdoc.load_tecdoc_manufacturer()
LoadDataTecdoc.load_tecdoc_manufacturer_model()
print('Load Data Tecdoc')
