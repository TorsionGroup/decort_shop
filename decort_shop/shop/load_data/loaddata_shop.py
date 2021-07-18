import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataShop:
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

    def load_managers(self):
        managers = self.client.service.GetData('managers')
        data = base64.b64decode(managers)
        file = open('cache/managers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_manager_buffer (
            source_id character varying(300),
            inner_name character varying(250),
            email character varying(250),
            phone character varying(250),
            is_active boolean );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/managers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_manager_buffer', columns=('source_id', 'inner_name', 'email', 'phone',
                                                                'is_active'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_manager m
            SET               
               inner_name  = b.inner_name,
               email  = b.email,
               phone  = b.phone,
               is_active = b.is_active               
            FROM shop_manager_buffer b
            WHERE m.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_customers(self):
        customers = self.client.service.GetData('customers')
        data = base64.b64decode(customers)
        file = open('cache/customers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_customer_buffer (
            source_id character varying(300),
            main_customer_id character varying(300),
            manager_id character varying(300),
            code character varying(300),
            name character varying(250),
            sale_policy character varying(300),
            city character varying(300),
            region_id character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_customer_buffer', columns=(
                'source_id', 'main_customer_id', 'manager_id', 'code', 'name', 'sale_policy', 'city', 'region_id'),
                          sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_customer c
            SET               
                code = b.code, 
                name = b.name, 
                sale_policy = b.sale_policy, 
                city = b.city, 
                region_id = b.region_id             
            FROM shop_customer_buffer b
            WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customer c
            SET manager_id_id = m.id                               
            FROM shop_manager m
            WHERE c.manager = m.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customer p
            SET main_customer_id_id = c.id
            FROM shop_customer c
            WHERE p.main_customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_currencies(self):
        currencies = self.client.service.GetData('currencies')
        data = base64.b64decode(currencies)
        file = open('cache/currencies.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_currency_buffer (
            code character varying(250),
            name character varying(250),
            title character varying(250),
            source_id character varying(300),
            rate numeric(15,2),
            mult integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/currencies.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_currency_buffer', columns=('source_id', 'code', 'name', 'title', 'rate', 'mult'),
                          sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_currency c
            SET
               code  = b.code,
               name  = b.name,
               title = b.title,
               rate  = b.rate,
               mult  = b.mult
            FROM shop_currency_buffer b
            WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_price_types(self):
        price_types = self.client.service.GetData('price_types')
        data = base64.b64decode(price_types)
        file = open('cache/price_types.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_pricetype_buffer (
            source_id character varying(300),
            name character varying(250) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/price_types.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_pricetype_buffer', columns=('source_id', 'name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_pricetype p
            SET               
                name  = b.name               
            FROM shop_pricetype_buffer b
            WHERE p.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_brands(self):
        brands = self.client.service.GetData('brands')
        data = base64.b64decode(brands)
        file = open('cache/brands.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_brand_buffer (
            source_id character varying(300),
            name character varying(250),
            supplier_id character varying(300),
            is_recommended boolean );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/brands.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_brand_buffer', columns=('source_id', 'name', 'supplier_id', 'is_recommended'),
                          sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_brand s
            SET               
                name  = b.name,
                supplier_id  = b.supplier_id,
                is_recommended  = b.is_recommended               
            FROM shop_brand_buffer b
            WHERE s.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_price_categories(self):
        price_categories = self.client.service.GetData('price_categories')
        data = base64.b64decode(price_categories)
        file = open('cache/price_categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_pricecategory_buffer (
            source_id character varying(300),
            inner_name character varying(250) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/price_categories.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_pricecategory_buffer', columns=('source_id', 'inner_name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_pricecategory p
            SET               
                inner_name  = b.inner_name               
            FROM shop_pricecategory_buffer b
            WHERE p.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_categories(self):
        categories = self.client.service.GetData('categories')
        data = base64.b64decode(categories)
        file = open('cache/categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_catalogcategory_buffer (
            source_id character varying(300),
            parent_source character varying(300),
            name_ru character varying(250),
            name_uk character varying(250),
            name_en character varying(250),
            url character varying(150),
            enabled boolean,
            level integer,
            lft integer,
            rght integer,
            tree_id integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/categories.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_catalogcategory_buffer',
                          columns=(
                          'source_id', 'parent_source', 'name_ru', 'name_uk', 'name_en', 'url', 'enabled', 'level',
                          'lft', 'rght', 'tree_id'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_catalogcategory p
            SET               
                parent_source = b.parent_source,
                name_ru = b.name_ru,
                name_uk = b.name_uk,
                name_en = b.name_en,
                url = b.url,
                enabled = b.enabled,
                level = b.level,
                lft = b.lft,
                rght = b.rght,
                tree_id = b.tree_id   
            FROM shop_catalogcategory_buffer b
            WHERE p.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_catalogcategory p
            SET parent_id = c.id
            FROM shop_catalogcategory c
            WHERE p.parent_source = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_offers(self):
        offers = self.client.service.GetData('offers')
        data = base64.b64decode(offers)
        file = open('cache/offers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_offer_buffer (
            source_id character varying(300),
            name character varying(250),
            group_name character varying(250),
            title character varying(250) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/offers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_offer_buffer',
                          columns=('source_id', 'name', 'group_name', 'title'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_offer o
            SET               
                name = b.name,
                group_name = b.group_name,
                title = b.title             
            FROM shop_offer_buffer b
            WHERE o.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

    def load_products(self):
        products = self.client.service.GetData('products')
        data = base64.b64decode(products)
        file = open('cache/products.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_product_buffer (
            source_id character varying(300),
            category character varying(300),
            brand character varying(300),
            offer character varying(300),
            code character varying(300),
            name_ru character varying(500),
            name_uk character varying(500),
            name_en character varying(500),
            comment_ru character varying(500),
            comment_uk character varying(500),
            comment_en character varying(500),
            article character varying(300),
            specification character varying(300),
            abc character varying(300),
            price_category character varying(300),
            advanced_description text,
            keywords_ru character varying(500),
            keywords_uk character varying(500),
            keywords_en character varying(500),
            manufacturer_name character varying(300),
            model_name character varying(300),            
            weight numeric(15,3),
            pack_qty integer,
            product_type integer,
            create_date character varying(300),
            income_date character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/products.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_product_buffer',
                          columns=(
                              'source_id', 'category', 'brand', 'offer', 'code', 'name_ru', 'name_uk', 'name_en',
                              'comment_ru', 'comment_uk', 'comment_en', 'article', 'specification', 'abc',
                              'price_category', 'advanced_description', 'keywords_ru', 'keywords_uk', 'keywords_en',
                              'manufacturer_name', 'model_name', 'weight', 'pack_qty', 'product_type',
                              'create_date', 'income_date'),
                          sep='|')
        self.conn.commit()

        ins_sql = '''INSERT INTO shop_product (source_id, code)
        SELECT source_id, code FROM shop_product_buffer
        WHERE source_id NOT IN(SELECT source_id FROM shop_product WHERE source_id IS NOT NULL);'''
        cur.execute(ins_sql)
        self.conn.commit()

        del_sql = '''DELETE FROM shop_product
        WHERE source_id NOT IN (SELECT source_id FROM shop_product_buffer);'''
        cur.execute(del_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shop_product p
            SET               
                category = b.category,
                brand = b.brand,
                offer = b.offer,
                code = b.code,
                name_ru = b.name_ru,
                name_uk = b.name_uk,
                name_en = b.name_en,
                comment_ru = b.comment_ru,
                comment_uk = b.comment_uk,
                comment_en = b.comment_en,
                article = b.article,
                specification = b.specification,
                abc = b.abc,
                price_category = b.price_category,
                advanced_description = b.advanced_description,
                keywords_ru = b.keywords_ru,
                keywords_uk = b.keywords_uk,
                keywords_en = b.keywords_en,
                manufacturer_name = b.manufacturer_name,
                model_name = b.model_name,
                weight = b.weight,
                pack_qty = b.pack_qty,
                product_type = b.product_type,
                create_date = b.create_date,
                income_date = b.income_date                       
            FROM shop_product_buffer b
            WHERE p.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shop_product p
            SET brand_id_id = b.id
            FROM shop_brand b
            WHERE p.brand = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shop_product p
            SET category_id_id = c.id
            FROM shop_catalogcategory c
            WHERE p.category = c.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        copy_sql = '''UPDATE shop_product p
            SET offer_id_id = o.id
            FROM shop_offer o
            WHERE p.offer = o.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()


LoadDataShop = LoadDataShop()
LoadDataShop.load_currencies()
LoadDataShop.load_price_types()
LoadDataShop.load_managers()
LoadDataShop.load_customers()
LoadDataShop.load_brands()
LoadDataShop.load_price_categories()
LoadDataShop.load_categories()
LoadDataShop.load_products()
LoadDataShop.load_offers()
print('Load Data Shop')
