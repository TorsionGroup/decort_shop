import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataDropshipping:
    def __init__(self):
        session = Session()
        session.auth = HTTPBasicAuth('Robot', 'Robot')
        transport = Transport(session=session, timeout=600)
        settings = Settings(xml_huge_tree=True)
        self.client = Client('http://192.168.75.104/live/ws/decort?wsdl', transport=transport,
                             settings=settings)

        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="decort_shop",
            user="torsion_prog",
            password="sdr%7ujK")

    def load_dropshipping_wallet(self):
        dropshipping_wallet = self.client.service.GetData('dropshipping_wallet')
        data = base64.b64decode(dropshipping_wallet)
        file = open('cache/dropshipping_wallet.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE dropshipping_dropshippingwallet_buffer (
                agreement character varying(300),
                order_order character varying(300), 
                credit numeric(15,2), 
                debit numeric(15,2), 
                balance numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/dropshipping_wallet.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'dropshipping_dropshippingwallet_buffer',
                          columns=('agreement', 'order_order', 'credit', 'debit', 'balance'), sep='|')
        self.conn.commit()

        ins_sql='''INSERT INTO dropshipping_dropshippingwallet (agreement, order_order)
                    SELECT agreement, order_order FROM dropshipping_dropshippingwallet_buffer
                    WHERE order_order NOT IN (SELECT order_order FROM dropshipping_dropshippingwallet WHERE order_order IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM dropshipping_dropshippingwallet
                        WHERE order_order NOT IN (SELECT order_order FROM dropshipping_dropshippingwallet_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE dropshipping_dropshippingwallet d
                SET
                    agreement = b.agreement,
                    credit = b.credit, 
                    debit = b.debit,
                    balance = b.balance            
                FROM dropshipping_dropshippingwallet_buffer b
                WHERE d.order_order = b.order_order;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE dropshipping_dropshippingwallet b
            SET agreement_id_id = c.id                               
            FROM customers_customeragreement c
            WHERE b.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE dropshipping_dropshippingwallet d
            SET order_id_id = o.id                               
            FROM orders_order o
            WHERE d.order_order = o.order_source;'''
        cur.execute(upd_sql)
        self.conn.commit()

LoadDataDropshipping = LoadDataDropshipping()
LoadDataDropshipping.load_dropshipping_wallet()
print('Load Data Dropshipping')
