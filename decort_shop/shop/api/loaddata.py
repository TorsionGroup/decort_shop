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

    def load_managers(self):
        managers = self.client.service.GetData('managers')
        data = base64.b64decode(managers)
        file = open('cache/managers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_manager_buffer (
            source_id character varying(300),
            inner_name character varying(250) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/managers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_manager_buffer', columns=('source_id', 'inner_name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_manager m
            SET               
               inner_name  = b.inner_name               
            FROM shop_manager_buffer b
            WHERE m.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()
        self.conn.close()

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
        self.conn.close()

    def load_brands(self):
        brands = self.client.service.GetData('brands')
        data = base64.b64decode(brands)
        file = open('cache/brands.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_brand_buffer (
            source_id character varying(300),
            name character varying(250) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/brands.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_brand_buffer', columns=('source_id', 'name'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_brand s
            SET               
                name  = b.name               
            FROM shop_brand_buffer b
            WHERE s.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()
        self.conn.close()

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
            rate numeric(15,5),
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
        self.conn.close()

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
        self.conn.close()

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
        self.conn.close()

    def load_categories(self):
        categories = self.client.service.GetData('categories')
        data = base64.b64decode(categories)
        file = open('cache/categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_catalogcategory_buffer (
            source_id character varying(300),
            parent character varying(300),
            name_ru character varying(250),
            name_uk character varying(250),
            name_en character varying(250),
            enabled boolean,
            level integer,
            lft integer,
            rght integer,
            tree_id integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/categories.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_catalogcategory_buffer',
                          columns=('source_id', 'parent', 'name_ru', 'name_uk', 'name_en', 'enabled', 'level', 'lft',
                                   'rght', 'tree_id'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_catalogcategory p
            SET               
                parent = b.parent,
                name_ru = b.name_ru,
                name_uk = b.name_uk,
                name_en = b.name_en,
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
            SET parent_id_id = c.id
            FROM shop_catalogcategory c
            WHERE p.parent = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_product_price_categories(self):
        product_price_categories = self.client.service.GetData('product_price_categories')
        data = base64.b64decode(product_price_categories)
        file = open('cache/product_price_categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

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
        self.conn.close()

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
                          'comment_ru', 'comment_uk', 'comment_en', 'article', 'specification', 'abc', 'price_category',
                          'advanced_description', 'weight', 'pack_qty', 'product_type', 'create_date',
                          'income_date'), sep='|')
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
        self.conn.close()

    def load_customer_points(self):
        customer_points = self.client.service.GetData('customer_points')
        data = base64.b64decode(customer_points)
        file = open('cache/customer_points.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_customerpoint_buffer (
            customer character varying(300),        
            source_id character varying(300),
            name character varying(300),
            add character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_points.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_customerpoint_buffer',
                          columns=('customer', 'source_id', 'name', 'add'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_customerpoint c
            SET 
                customer = b.customer,              
                name = b.name,
                add = b.add                           
            FROM shop_customerpoint_buffer b
            WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customerpoint p
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE p.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_customer_agreements(self):
        customer_agreements = self.client.service.GetData('customer_agreements')
        data = base64.b64decode(customer_agreements)
        file = open('cache/customer_agreements.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_customeragreement_buffer (
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
            cur.copy_from(file, 'shop_customeragreement_buffer',
                          columns=('source_id', 'customer', 'currency', 'price_type',
                                   'code', 'name', 'number', 'discount', 'is_status', 'is_active'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_customeragreement c
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
            FROM shop_customeragreement_buffer b
            WHERE c.source_id = b.source_id;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customeragreement a
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE a.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customeragreement a
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE a.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customeragreement a
            SET price_type_id_id = p.id                               
            FROM shop_pricetype p
            WHERE a.price_type = p.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_balances(self):
        balances = self.client.service.GetData('balances')
        data = base64.b64decode(balances)
        file = open('cache/balances.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_balance_buffer (
            customer character varying(300),
            agreement character varying(300), 
            currency character varying(300), 
            balance numeric(15,2), 
            past_due numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/balances.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_balance_buffer',
                          columns=('customer', 'agreement', 'currency', 'balance', 'past_due'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_balance c
            SET
                agreement = b.agreement,
                currency = b.currency, 
                balance = b.balance, 
                past_due = b.past_due            
            FROM shop_balance_buffer b
            WHERE c.customer = b.customer;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_balance a
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE a.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_balance a
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE a.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_balance b
            SET agreement_id_id = c.id                               
            FROM shop_customeragreement c
            WHERE b.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_customer_discounts(self):
        customer_discounts = self.client.service.GetData('customer_discounts')
        data = base64.b64decode(customer_discounts)
        file = open('cache/customer_discounts.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_customerdiscount_buffer (
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
            cur.copy_from(file, 'shop_customerdiscount_buffer',
                          columns=('source_id', 'brand', 'customer', 'agreement',
                                   'price_type', 'criteria_type', 'discount'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_customerdiscount c
            SET
                source_id = b.source_id,
                brand = b.brand,
                agreement = b.agreement, 
                price_type = b.price_type, 
                criteria_type = b.criteria_type,
                discount = b.discount            
            FROM shop_customerdiscount_buffer b
            WHERE c.customer= b.customer;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customerdiscount a
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE a.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customerdiscount a
            SET price_type_id_id = c.id                               
            FROM shop_pricetype c
            WHERE a.price_type = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_customerdiscount b
            SET agreement_id_id = c.id                               
            FROM shop_customeragreement c
            WHERE b.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_dropshipping_wallet(self):
        dropshipping_wallet = self.client.service.GetData('dropshipping_wallet')
        data = base64.b64decode(dropshipping_wallet)
        file = open('cache/dropshipping_wallet.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_dropshippingwallet_buffer (
                agreement character varying(300),
                order_order character varying(300), 
                credit numeric(15,2), 
                debit numeric(15,2), 
                balance numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/dropshipping_wallet.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_dropshippingwallet_buffer',
                          columns=('agreement', 'order_order', 'credit', 'debit', 'balance'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_dropshippingwallet d
                SET
                    agreement = b.agreement,
                    credit = b.credit, 
                    debit = b.debit,
                    balance = b.balance            
                FROM shop_dropshippingwallet_buffer b
                WHERE d.order_order = b.order_order;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_dropshippingwallet b
            SET agreement_id_id = c.id                               
            FROM shop_customeragreement c
            WHERE b.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_dropshippingwallet d
            SET order_id_id = o.id                               
            FROM shop_order o
            WHERE d.order_order = o.order_source;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_prices(self):
        prices = self.client.service.GetData('prices')
        data = base64.b64decode(prices)
        file = open('cache/prices.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_price_buffer (
            product character varying(300),
            price_type character varying(300), 
            currency character varying(300), 
            price numeric(15,2) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/prices.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_price_buffer',
                          columns=('product', 'price_type', 'currency', 'price'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_price p
            SET
                price_type = b.price_type,
                currency = b.currency, 
                price = b.price          
            FROM shop_price_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_price p
            SET price_type_id_id = c.id                               
            FROM shop_pricetype c
            WHERE p.price_type = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_price p
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE p.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_price p
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE p.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_sales(self):
        sales = self.client.service.GetData('sales')
        data = base64.b64decode(sales)
        file = open('cache/sales.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_sale_buffer (
            product character varying(300),
            customer character varying(300), 
            qty integer, 
            date character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/sales.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_sale_buffer', columns=('product', 'customer', 'qty', 'date'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_sale s
            SET
                customer = b.customer,
                qty = b.qty, 
                date = b.date          
            FROM shop_sale_buffer b
            WHERE s.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_sale s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_sale s
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE s.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_sale_tasks(self):
        sale_tasks = self.client.service.GetData('sale_tasks')
        data = base64.b64decode(sale_tasks)
        file = open('cache/sale_tasks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_saletask_buffer (
            product character varying(300),
            customer character varying(300), 
            qty integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/sale_tasks.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_saletask_buffer',
                          columns=('product', 'customer', 'qty'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_saletask s
            SET
                customer = b.customer,
                qty = b.qty                             
            FROM shop_saletask_buffer b
            WHERE s.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_saletask s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_saletask s
            SET customer_id_id = c.id                               
            FROM shop_customer c
            WHERE s.customer = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_stocks(self):
        stocks = self.client.service.GetData('stocks')
        data = base64.b64decode(stocks)
        file = open('cache/stocks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_stock_buffer (
            product character varying(300),
            stock_name character varying(300), 
            amount_total integer, 
            amount_account integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/stocks.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_stock_buffer',
                          columns=('product', 'stock_name', 'amount_total', 'amount_account'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_stock s
            SET
                stock_name = b.stock_name,
                amount_total = b.amount_total, 
                amount_account = b.amount_account                             
            FROM shop_stock_buffer b
            WHERE s.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_stock s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_deficit(self):
        deficit = self.client.service.GetData('deficit')
        data = base64.b64decode(deficit)
        file = open('cache/deficit.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_deficitreserve_buffer (
            product character varying(300),
            sale_policy character varying(300), 
            amount integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/deficit.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_deficitreserve_buffer',
                          columns=('product', 'sale_policy', 'amount'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_deficitreserve d
            SET
                sale_policy = b.sale_policy,
                amount = b.amount                         
            FROM shop_deficitreserve_buffer b
            WHERE d.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_deficitreserve d
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE d.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_description(self):
        description = self.client.service.GetData('description')
        data = base64.b64decode(description)
        file = open('cache/description.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_productdescription_buffer (
            product character varying(300),
            property character varying(300), 
            value text );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/description.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_productdescription_buffer',
                          columns=('product', 'property', 'value'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_productdescription p
            SET
                property = b.property,
                value = b.value                         
            FROM shop_productdescription_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_productdescription d
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE d.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_applicability(self):
        applicability = self.client.service.GetData('applicability')
        data = base64.b64decode(applicability)
        file = open('cache/applicability.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_productapplicability_buffer (
            product character varying(300),
            vehicle character varying(300),
            modification character varying(300), 
            engine character varying(300), 
            year character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/applicability.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_productapplicability_buffer',
                          columns=('product', 'vehicle', 'modification', 'engine', 'year'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_productapplicability p
            SET
                vehicle = b.vehicle,
                modification = b.modification,
                engine = b.engine,
                year = b.year                         
            FROM shop_productapplicability_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_productapplicability a
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE a.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_cross(self):
        cross = self.client.service.GetData('cross')
        data = base64.b64decode(cross)
        file = open('cache/cross.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_cross_buffer (
            product character varying(300),
            brand character varying(300),                
            article_nr character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/cross.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_cross_buffer',
                          columns=('product', 'brand', 'article_nr'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_cross p
            SET
                brand = b.brand,
                article_nr = b.article_nr                       
            FROM shop_cross_buffer b
            WHERE p.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_cross s
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE s.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_orders(self):
        orders = self.client.service.GetData('orders')
        data = base64.b64decode(orders)
        file = open('cache/orders.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_order_buffer (
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
            cur.copy_from(file, 'shop_order_buffer',
                      columns=('order_source', 'agreement', 'order_number', 'waybill_number',
                               'comment', 'source_type', 'has_precept', 'has_waybill', 'order_date'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_order o
            SET
                agreement = b.agreement,
                order_number = b.order_number,
                waybill_number = b.waybill_number,
                comment = b.comment,
                source_type = b.source_type,
                has_precept = b.has_precept,
                has_waybill = b.has_waybill,
                order_date = b.order_date                                       
            FROM shop_order_buffer b
            WHERE o.order_source = b.order_source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_order o
            SET agreement_id_id = c.id                               
            FROM shop_customeragreement c
            WHERE o.agreement = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_order_items(self):
        order_items = self.client.service.GetData('order_items')
        data = base64.b64decode(order_items)
        file = open('cache/order_items.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_orderitem_buffer (
            order_source character varying(300),
            product character varying(300),                
            currency character varying(300),
            qty integer,
            price numeric(15, 2),
            reserved integer,
            executed integer );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/order_items.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_orderitem_buffer',
                      columns=('order_source', 'product', 'currency', 'qty', 'price', 'reserved', 'executed'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_orderitem o
            SET
                product = b.product,
                currency = b.currency,
                qty = b.qty,
                price = b.price,
                reserved = b.reserved,
                executed = b.executed                            
            FROM shop_orderitem_buffer b
            WHERE o.order_source = b.order_source;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_orderitem o
            SET product_id_id = p.id                               
            FROM shop_product p
            WHERE o.product = p.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_orderitem o
            SET currency_id_id = c.id                               
            FROM shop_currency c
            WHERE o.currency = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

        upd_sql = '''UPDATE shop_orderitem o
            SET order_id_id = c.id                               
            FROM shop_order c
            WHERE o.order_source = c.order_source;'''
        cur.execute(upd_sql)
        self.conn.commit()
        self.conn.close()

    def load_declaration_numbers(self):
        declaration_numbers = self.client.service.GetData('declaration_numbers')
        data = base64.b64decode(declaration_numbers)
        file = open('cache/declaration_numbers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_declarationnumber_buffer (
            order_source character varying(300),
            declaration_number character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/declaration_numbers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_declarationnumber_buffer',
                          columns=('order_source', 'declaration_number'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE shop_order o
            SET
                declaration_number = b.declaration_number                       
            FROM shop_declarationnumber_buffer b
            WHERE o.order_source = b.order_source;'''
        cur.execute(copy_sql)
        self.conn.commit()
        self.conn.close()


loadData = LoadData()
# loadData.load_managers()
# loadData.load_customers()
# loadData.load_brands()
# loadData.load_currencies()
# loadData.load_price_types()
# loadData.load_price_categories()
# loadData.load_categories()
# loadData.load_product_price_categories()
# loadData.load_offers()
# loadData.load_products()
# loadData.load_customer_points()
# loadData.load_customer_agreements()
# loadData.load_balances()
# loadData.load_customer_discounts()
# loadData.load_dropshipping_wallet()
# loadData.load_prices()
# loadData.load_sales()
# loadData.load_sale_tasks()
# loadData.load_stocks()
# loadData.load_deficit()
# loadData.load_description()
# loadData.load_applicability()
# loadData.load_cross()
# loadData.load_orders()
loadData.load_order_items()
# loadData.load_declaration_numbers()
