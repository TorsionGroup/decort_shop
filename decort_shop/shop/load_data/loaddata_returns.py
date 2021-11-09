import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataReturns:
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

    def load_returns(self):
        returns = self.client.service.GetData('returns')
        data = base64.b64decode(returns)
        file = open('cache/returns.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE returns_proformreturn_buffer (
            source character varying(300),
            source_customer character varying(300),
            source_agreement character varying(300),
            source_order character varying(300),
            comment character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/returns.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'returns_proformreturn_buffer',
                          columns=('source', 'source_customer', 'source_agreement', 'source_order', 'comment'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE returns_proformreturn r
            SET
                source_customer = b.source_customer,
                source_agreement = b.source_agreement,
                source_order = b.source_order,
                comment = b.comment       
            FROM returns_proformreturn_buffer b
            WHERE r.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()


LoadDataReturns = LoadDataReturns()
LoadDataReturns.load_returns()
print('Load Data Returns')
