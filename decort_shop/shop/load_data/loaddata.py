import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadData:
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
            is_active boolean );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/managers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_manager_buffer', columns=('source_id', 'inner_name', 'is_active'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_manager m
            SET               
               inner_name  = b.inner_name,
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
                              'price_category',
                              'advanced_description', 'keywords_ru', 'keywords_uk', 'keywords_en', 'manufacturer_name',
                              'model_name', 'weight', 'pack_qty', 'product_type', 'create_date', 'income_date'),
                          sep='|')
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


class LoadDataCustomers:
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
            is_user boolean,
            birthday character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_contacts.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customercontact_buffer',
                          columns=('source', 'source_customer', 'name', 'email', 'is_user', 'birthday'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE customers_customercontact c
            SET 
                source_customer = b.source_customer,              
                name = b.name,
                email = b.email,              
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
            add character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_points.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customerpoint_buffer',
                          columns=('customer', 'source_id', 'name', 'add'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE customers_customerpoint c
            SET 
                customer = b.customer,              
                name = b.name,
                add = b.add                           
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
            is_active boolean );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_agreements.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'customers_customeragreement_buffer',
                          columns=('source_id', 'customer', 'currency', 'price_type',
                                   'code', 'name', 'number', 'discount', 'is_status', 'is_active'), sep='|')
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
                is_active = b.is_active                                   
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


class LoadDataProducts:
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

    def load_product_price_categories(self):
        product_price_categories = self.client.service.GetData('product_price_categories')
        data = base64.b64decode(product_price_categories)
        file = open('cache/product_price_categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_product_price_categories_buffer (
            product_source character varying(300),
            price_categories_source character varying(300),
            product_name character varying(300),
            price_categories_name character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/product_price_categories.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_product_price_categories_buffer',
                          columns=('product_source', 'price_categories_source', 'product_name',
                                   'price_categories_name'), sep='|')
        self.conn.commit()

        upd_sql = '''UPDATE shop_product p
            SET price_category_id_id = c.id
            FROM shop_pricecategory c JOIN shop_product_price_categories_buffer b 
            ON c.source_id = b.price_categories_source
            WHERE p.source_id = b.product_source;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_prices(self):
        prices = self.client.service.GetData('prices')
        data = base64.b64decode(prices)
        file = open('cache/prices.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_price_buffer (
            product character varying(300),
            price_type character varying(300), 
            currency character varying(300), 
            price numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/prices.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_price_buffer',
                          columns=('product', 'price_type', 'currency', 'price'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_price p
            SET
                price_type = b.price_type,
                currency = b.currency, 
                price = b.price          
            FROM products_price_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_price p
            SET price_type_id_id = c.id                               
            FROM shop_pricetype c
            WHERE p.price_type = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_price p
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE p.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_price p
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE p.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_stocks(self):
        stocks = self.client.service.GetData('stocks')
        data = base64.b64decode(stocks)
        file = open('cache/stocks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_stock_buffer (
            product character varying(300),
            stock_name character varying(300), 
            amount_total integer, 
            amount_account integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/stocks.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_stock_buffer',
                          columns=('product', 'stock_name', 'amount_total', 'amount_account'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_stock s
            SET
                stock_name = b.stock_name,
                amount_total = b.amount_total, 
                amount_account = b.amount_account                             
            FROM products_stock_buffer b
            WHERE s.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_stock s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_deficit(self):
        deficit = self.client.service.GetData('deficit')
        data = base64.b64decode(deficit)
        file = open('cache/deficit.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_deficitreserve_buffer (
            product character varying(300),
            sale_policy character varying(300), 
            amount integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/deficit.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_deficitreserve_buffer',
                          columns=('product', 'sale_policy', 'amount'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_deficitreserve d
            SET
                sale_policy = b.sale_policy,
                amount = b.amount                         
            FROM products_deficitreserve_buffer b
            WHERE d.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_deficitreserve d
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE d.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_description(self):
        description = self.client.service.GetData('description')
        data = base64.b64decode(description)
        file = open('cache/description.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_productdescription_buffer (
            product character varying(300),
            property character varying(300), 
            value text );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/description.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_productdescription_buffer',
                          columns=('product', 'property', 'value'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_productdescription p
            SET
                property = b.property,
                value = b.value                         
            FROM products_productdescription_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_productdescription d
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE d.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_applicability(self):
        applicability = self.client.service.GetData('applicability')
        data = base64.b64decode(applicability)
        file = open('cache/applicability.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_productapplicability_buffer (
            product character varying(300),
            vehicle character varying(300),
            modification character varying(300), 
            engine character varying(300), 
            year character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/applicability.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_productapplicability_buffer',
                          columns=('product', 'vehicle', 'modification', 'engine', 'year'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_productapplicability p
            SET
                vehicle = b.vehicle,
                modification = b.modification,
                engine = b.engine,
                year = b.year                         
            FROM products_productapplicability_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_productapplicability a
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE a.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    def load_cross(self):
        cross = self.client.service.GetData('cross')
        data = base64.b64decode(cross)
        file = open('cache/cross.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_cross_buffer (
            product character varying(300),
            brand character varying(300),                
            article_nr character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/cross.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_cross_buffer',
                          columns=('product', 'brand', 'article_nr'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_cross p
            SET
                brand = b.brand,
                article_nr = b.article_nr                       
            FROM products_cross_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_cross s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()


class LoadDataOrders:
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


class LoadDataDropshipping:
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


class LoadDataShipping:
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


class LoadDataReturns:
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

LoadDataCustomers = LoadDataCustomers()
LoadDataCustomers.load_customer_contacts()
LoadDataCustomers.load_customer_agreements()
LoadDataCustomers.load_customer_discounts()
LoadDataCustomers.load_customer_points()
LoadDataCustomers.load_balances()
print('Load Data Customers')

LoadDataProducts = LoadDataProducts()
LoadDataProducts.load_cross()
LoadDataProducts.load_description()
LoadDataProducts.load_applicability()
LoadDataProducts.load_product_price_categories()
LoadDataProducts.load_prices()
LoadDataProducts.load_stocks()
LoadDataProducts.load_deficit()
print('Load Data Products')

LoadDataOrders = LoadDataOrders()
LoadDataOrders.load_orders()
LoadDataOrders.load_order_items()
LoadDataOrders.load_declaration_numbers()
print('Load Data Orders')

LoadDataDropshipping = LoadDataDropshipping()
LoadDataDropshipping.load_dropshipping_wallet()
print('Load Data Dropshipping')

LoadDataManagers = LoadDataManagers()
LoadDataManagers.load_sales()
LoadDataManagers.load_sale_tasks()
print('Load Data Managers')

LoadDataShipping = LoadDataShipping()
LoadDataShipping.load_regions()
print('Load Data Shipping')

LoadDataReturns = LoadDataReturns()
LoadDataReturns.load_returns()
print('Load Data Returns')
