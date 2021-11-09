import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataOrders:
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

    def load_orders(self):
        orders = self.client.service.GetData('orders')
        data = base64.b64decode(orders)
        file = open('cache/orders.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE orders_order_buffer (
            order_source character varying(300),
            agreement character varying(300),                
            order_number character varying(300),
            waybill_number character varying(300),
            comment character varying(300),
            source_type character varying(300),
            has_precept boolean,
            has_waybill boolean,
            order_date character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/orders.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'orders_order_buffer',
                          columns=('order_source', 'agreement', 'order_number', 'waybill_number',
                                   'comment', 'source_type', 'has_precept', 'has_waybill', 'order_date'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE orders_order o
            SET
                agreement = b.agreement,
                order_number = b.order_number,
                waybill_number = b.waybill_number,
                comment = b.comment,
                source_type = b.source_type,
                has_precept = b.has_precept,
                has_waybill = b.has_waybill,
                order_date = b.order_date                                       
            FROM orders_order_buffer b
            WHERE o.order_source = b.order_source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE orders_order o
            SET agreement_id_id = c.id                               
            FROM customers_customeragreement c
            WHERE o.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_order_items(self):
        order_items = self.client.service.GetData('order_items')
        data = base64.b64decode(order_items)
        file = open('cache/order_items.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE orders_orderitem_buffer (
            order_source character varying(300),
            product_source character varying(300),                
            currency_source character varying(300),
            quantity integer,
            price numeric(15, 2),
            reserved integer,
            executed integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/order_items.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'orders_orderitem_buffer',
                          columns=('order_source', 'product_source', 'currency_source', 'quantity', 'price', 'reserved',
                                   'executed'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE orders_orderitem o
            SET
                product_source = b.product_source,
                currency_source = b.currency_source,
                quantity = b.quantity,
                price = b.price,
                reserved = b.reserved,
                executed = b.executed                            
            FROM orders_orderitem_buffer b
            WHERE o.order_source = b.order_source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE orders_orderitem o
            SET product_id = p.id                               
            FROM shop_product p
            WHERE o.product_source = p.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE orders_orderitem o
            SET currency_id = c.id                               
            FROM shop_currency c
            WHERE o.currency_source = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE orders_orderitem o
            SET order_id = c.id                               
            FROM orders_order c
            WHERE o.order_source = c.order_source;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_declaration_numbers(self):
        declaration_numbers = self.client.service.GetData('declaration_numbers')
        data = base64.b64decode(declaration_numbers)
        file = open('cache/declaration_numbers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE orders_declarationnumber_buffer (
            order_source character varying(300),
            declaration_number character varying(300),
            declaration_number_status character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/declaration_numbers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'orders_declarationnumber_buffer',
                          columns=('order_source', 'declaration_number', 'declaration_number_status'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE orders_order o
            SET
                declaration_number = b.declaration_number, 
                declaration_number_status = b.declaration_number_status                      
            FROM orders_declarationnumber_buffer b
            WHERE o.order_source = b.order_source;'''
        cur.execute(copy_sql)
        self.conn.commit()


LoadDataOrders = LoadDataOrders()
LoadDataOrders.load_orders()
LoadDataOrders.load_order_items()
LoadDataOrders.load_declaration_numbers()
print('Load Data Orders')
