import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataCustomers:
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

    def load_customer_contacts(self):
        customer_contacts = self.client.service.GetData('customer_contacts')
        data = base64.b64decode(customer_contacts)
        file = open('cache/customer_contacts.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE customers_customercontact_buffer (
            source character varying(300),        
            source_customer character varying(300),
            name character varying(300),
            email character varying(300),
            phone character varying(300),
            is_user boolean,
            birthday character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_contacts.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customercontact_buffer',
                          columns=('source', 'source_customer', 'name', 'email', 'phone', 'is_user', 'birthday'),
                          sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO customers_customercontact (source, source_customer, name)
                 SELECT source, source_customer, name FROM customers_customercontact_buffer
                 WHERE source NOT IN (SELECT source FROM customers_customercontact WHERE source IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM customers_customercontact
                 WHERE source NOT IN (SELECT source FROM customers_customercontact_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE customers_customercontact c
            SET 
                source_customer = b.source_customer,              
                name = b.name,
                email = b.email,
                phone = b.phone,               
                is_user = b.is_user,
                birthday = b.birthday                           
            FROM customers_customercontact_buffer b
            WHERE c.source = b.source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customercontact p
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE p.source_customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_customer_points(self):
        customer_points = self.client.service.GetData('customer_points')
        data = base64.b64decode(customer_points)
        file = open('cache/customer_points.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE customers_customerpoint_buffer (
            customer character varying(300),        
            source_id character varying(300),
            name character varying(300),
            add character varying(300),
            latitude character varying(300),
            longitude character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_points.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customerpoint_buffer',
                          columns=('customer', 'source_id', 'name', 'add', 'latitude', 'longitude'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO customers_customerpoint (customer, source_id, name)
                 SELECT customer, source_id, name FROM customers_customerpoint_buffer
                 WHERE source_id NOT IN (SELECT source_id FROM customers_customerpoint WHERE source_id IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM customers_customerpoint
                 WHERE source_id NOT IN (SELECT source_id FROM customers_customerpoint_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE customers_customerpoint c
            SET 
                customer = b.customer,              
                name = b.name,
                add = b.add,
                latitude = b.latitude,
                longitude = b.longitude                           
            FROM customers_customerpoint_buffer b
            WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customerpoint p
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE p.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_customer_points_gps(self):
        customer_points_gps = self.client.service.GetData('customer_points_gps')
        data = base64.b64decode(customer_points_gps)
        file = open('cache/customer_points_gps.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE customers_customerpointgps_buffer (
                    customer character varying(300),        
                    source_id character varying(300),
                    region_id character varying(300),
                    name character varying(300),
                    add_name character varying(300),
                    extra_name character varying(300),
                    oblast character varying(300),
                    area_ref character varying(300),
                    city character varying(300),
                    settlement_type character varying(300),
                    settlement_type_description character varying(300),
                    city_ref character varying(300),
                    street character varying(300),
                    street_type_ref character varying(300),
                    street_type character varying(300),
                    street_ref character varying(300),
                    extra_street character varying(300),
                    house_number character varying(300),
                    comments character varying(300),
                    latitude character varying(300),
                    longitude character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_points_gps.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customerpointgps_buffer',
                          columns=('customer', 'source_id', 'region_id', 'name', 'add_name', 'extra_name', 'oblast',
                                   'area_ref', 'city', 'settlement_type', 'settlement_type_description', 'city_ref',
                                   'street', 'street_type_ref', 'street_type', 'street_ref', 'extra_street',
                                   'house_number', 'comments', 'latitude', 'longitude'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO customers_customerpointgps (customer, source_id, name)
                         SELECT customer, source_id, name FROM customers_customerpointgps_buffer
                         WHERE source_id NOT IN (SELECT source_id FROM customers_customerpointgps WHERE source_id IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM customers_customerpointgps
                         WHERE source_id NOT IN (SELECT source_id FROM customers_customerpointgps_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE customers_customerpointgps c
                    SET 
                        customer = b.customer, 
                        region_id = b.region_id,             
                        name = b.name,
                        add_name = b.add_name,
                        extra_name = b.extra_name,
                        oblast = b.oblast,
                        area_ref = b.area_ref,
                        city = b.city,
                        settlement_type = b.settlement_type,
                        settlement_type_description = b.settlement_type_description,
                        city_ref = b.city_ref,
                        street = b.street,
                        street_type_ref = b.street_type_ref,
                        street_type = b.street_type,
                        street_ref = b.street_ref,
                        extra_street = b.extra_street,
                        house_number = b.house_number,
                        comments = b.comments,
                        latitude = b.latitude,
                        longitude = b.longitude                           
                    FROM customers_customerpointgps_buffer b
                    WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customerpointgps p
                    SET customer_id_id = c.id                               
                    FROM shop_customer c
                    WHERE p.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_customer_agreements(self):
        customer_agreements = self.client.service.GetData('customer_agreements')
        data = base64.b64decode(customer_agreements)
        file = open('cache/customer_agreements.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE customers_customeragreement_buffer (
            source_id character varying(300),
            customer character varying(300), 
            currency character varying(300), 
            price_type character varying(300), 
            code character varying(300), 
            name character varying(300),
            number character varying(300),
            discount numeric(15,2),
            is_status boolean,
            is_active boolean,
            finish_date character varying(300)  );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_agreements.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customeragreement_buffer',
                          columns=('source_id', 'customer', 'currency', 'price_type',
                                   'code', 'name', 'number', 'discount', 'is_status', 'is_active', 'finish_date'),
                          sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO customers_customeragreement (source_id, customer, name)
                         SELECT source_id, customer, name FROM customers_customeragreement_buffer
                         WHERE source_id NOT IN (SELECT source_id FROM customers_customeragreement WHERE source_id IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM customers_customeragreement
                         WHERE source_id NOT IN (SELECT source_id FROM customers_customeragreement_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE customers_customeragreement c
            SET
                customer = b.customer,
                currency = b.currency,
                price_type = b.price_type,
                code = b.code,
                name = b.name,               
                number = b.number,
                discount = b.discount,
                is_status = b.is_status,
                is_active = b.is_active,
                finish_date = b.finish_date                                    
            FROM customers_customeragreement_buffer b
            WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customeragreement a
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE a.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customeragreement a
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE a.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customeragreement a
            SET price_type_id_id = p.id                               
            FROM shop_pricetype p
            WHERE a.price_type = p.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_balances(self):
        balances = self.client.service.GetData('balances')
        data = base64.b64decode(balances)
        file = open('cache/balances.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE customers_balance_buffer (
            customer character varying(300),
            agreement character varying(300), 
            currency character varying(300), 
            balance numeric(15,2), 
            past_due numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/balances.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_balance_buffer',
                          columns=('customer', 'agreement', 'currency', 'balance', 'past_due'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO customers_balance (customer, agreement)
                        SELECT customer, agreement FROM customers_balance_buffer
                        WHERE customer NOT IN (SELECT customer FROM customers_balance WHERE customer IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM customers_balance
                        WHERE customer NOT IN (SELECT customer FROM customers_balance_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE customers_balance c
            SET
                agreement = b.agreement,
                currency = b.currency, 
                balance = b.balance, 
                past_due = b.past_due            
            FROM customers_balance_buffer b
            WHERE c.customer = b.customer;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_balance a
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE a.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_balance a
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE a.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_balance b
            SET agreement_id_id = c.id                               
            FROM customers_customeragreement c
            WHERE b.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_customer_discounts(self):
        customer_discounts = self.client.service.GetData('customer_discounts')
        data = base64.b64decode(customer_discounts)
        file = open('cache/customer_discounts.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE customers_customerdiscount_buffer (
            source_id character varying(300),
            brand character varying(300),
            customer character varying(300), 
            agreement character varying(300), 
            price_type character varying(300), 
            criteria_type character varying(300), 
            discount numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_discounts.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customerdiscount_buffer',
                          columns=('source_id', 'brand', 'customer', 'agreement',
                                   'price_type', 'criteria_type', 'discount'), sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO customers_customerdiscount (source_id, customer)
                        SELECT source_id, customer FROM customers_customerdiscount_buffer
                        WHERE source_id NOT IN (SELECT source_id FROM customers_balance WHERE source_id IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM customers_customerdiscount
                        WHERE source_id NOT IN (SELECT source_id FROM customers_customerdiscount_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE customers_customerdiscount c
            SET
                source_id = b.source_id,
                brand = b.brand,
                agreement = b.agreement, 
                price_type = b.price_type, 
                criteria_type = b.criteria_type,
                discount = b.discount            
            FROM customers_customerdiscount_buffer b
            WHERE c.customer= b.customer;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customerdiscount a
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE a.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customerdiscount a
            SET price_type_id_id = c.id                               
            FROM shop_pricetype c
            WHERE a.price_type = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE customers_customerdiscount b
            SET agreement_id_id = c.id                               
            FROM customers_customeragreement c
            WHERE b.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()


LoadDataCustomers = LoadDataCustomers()
# LoadDataCustomers.load_customer_contacts()
# LoadDataCustomers.load_customer_agreements()
# LoadDataCustomers.load_customer_discounts()
LoadDataCustomers.load_customer_points()
LoadDataCustomers.load_customer_points_gps()
# LoadDataCustomers.load_balances()
print('Load Data Customers')
