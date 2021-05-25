import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataUsers:
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

    def load_users(self):
        cur = self.conn.cursor()

        copy_sql = '''UPDATE shop_account a
            SET              
                username = b.name,
                email = b.email,
                phone = b.phone,               
                is_active = b.is_user,
                date_of_birth = b.birthday                         
            FROM customers_customercontact b
            WHERE customer_id_id = b.customer_id_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_new_users(self):
        cur = self.conn.cursor()

        copy_sql = '''INSERT INTO shop_account (username, email, phone, is_active, date_of_birth, customer_id_id)
            SELECT name, email, phone, is_user, birthday, customer_id_id                           
            FROM customers_customercontact b
            WHERE b.customer_id_id IS NOT NULL;'''
        cur.execute(copy_sql)
        self.conn.commit()


LoadDataUsers = LoadDataUsers()
# LoadDataUsers.load_users()
# LoadDataUsers.load_new_users()
print('Load Data Users')
