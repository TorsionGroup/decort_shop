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

    def load_tecdoc_manufacturer_model(self):
        tecdoc_manufacturer_model = self.client.service.GetData('tecdoc_manufacturer_model')
        data = base64.b64decode(tecdoc_manufacturer_model)
        file = open('cache/tecdoc_manufacturer_model.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()


LoadDataTecdoc = LoadDataTecdoc()
LoadDataTecdoc.load_tecdoc_manufacturer()
LoadDataTecdoc.load_tecdoc_manufacturer_model()
print('Load Data Tecdoc')
