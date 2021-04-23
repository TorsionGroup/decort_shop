import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataManagers:
    def __init__(self):
        session = Session()
        session.auth = HTTPBasicAuth('Robot', 'Robot')
        transport = Transport(session=session, timeout=600)
        settings = Settings(xml_huge_tree=True)
        self.client = Client('http://192.168.75.115:8005/live/ws/decort?wsdl', transport=transport,
                             settings=settings)

        self.conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="decort_shop",
            user="torsion_prog",
            password="sdr%7ujK")

    def load_sales(self):
        sales = self.client.service.GetData('sales')
        data = base64.b64decode(sales)
        file = open('cache/sales.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE managers_sale_buffer (
            product character varying(300),
            customer character varying(300), 
            qty integer, 
            date character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/sales.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'managers_sale_buffer', columns=('product', 'customer', 'qty', 'date'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE managers_sale s
            SET
                customer = b.customer,
                qty = b.qty, 
                date = b.date          
            FROM managers_sale_buffer b
            WHERE s.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE managers_sale s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE managers_sale s
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE s.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_sale_tasks(self):
        sale_tasks = self.client.service.GetData('sale_tasks')
        data = base64.b64decode(sale_tasks)
        file = open('cache/sale_tasks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE managers_saletask_buffer (
            product character varying(300),
            customer character varying(300), 
            qty integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/sale_tasks.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'managers_saletask_buffer',
                          columns=('product', 'customer', 'qty'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE managers_saletask s
            SET
                customer = b.customer,
                qty = b.qty                             
            FROM managers_saletask_buffer b
            WHERE s.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE managers_saletask s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE managers_saletask s
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE s.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()


LoadDataManagers = LoadDataManagers()
LoadDataManagers.load_sales()
LoadDataManagers.load_sale_tasks()
print('Load Data Managers')
