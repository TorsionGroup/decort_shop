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
        self.client = Client('http://192.168.75.115:8005/alexey/ws/decort?wsdl', transport=transport, settings=settings)

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
            name character varying(250));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/managers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_manager_buffer', columns=('source_id', 'name'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_manager m
            SET               
               inner_name  = b.name,               
            FROM shop_currency_buffer b
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
            main_source_id character varying(300),
            manager_source_id character varying(300),
            code character varying(300),
            name character varying(250)
            sale_policy character varying(300),
            city character varying(300),
            region_id character varying(300));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_customer_buffer', columns=(
                'source_id', 'main_source_id', 'manager_source_id', 'code', 'name', 'sale_policy', 'city', 'region_id'),
                          sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_customer c
            SET               
                main_source_id  = b.main_source_id,  
                manager_source_id = b.manager_source_id, 
                code = b.code, 
                name = b.name, 
                sale_policy = b.sale_policy, 
                city = b.city, 
                region_id = b.region_id,             
            FROM shop_customer_buffer b
            WHERE c.source_id = b.source_id;'''

        cur.execute(copy_sql)
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
            name character varying(250));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/brands.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_brand_buffer', columns=('source_id', 'name'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_brand s
            SET               
                name  = b.name,               
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

        t_sql = '''CREATE TEMP TABLE shop_price_type_buffer (
            source_id character varying(300),
            name character varying(250));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/price_types.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_price_type_buffer', columns=('source_id', 'name'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_price_type p
            SET               
                name  = b.name,               
            FROM shop_price_type_buffer b
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

        t_sql = '''CREATE TEMP TABLE shop_price_category_buffer (
            source_id character varying(300),
            inner_name character varying(250));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/price_categories.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_price_category_buffer', columns=('source_id', 'inner_name'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_price_category p
            SET               
                inner_name  = b.inner_name,               
            FROM shop_price_category_buffer b
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
            parent_id character varying(300)
            name character varying(250)
            name_ukr character varying(250)
            name character varying(250));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/categories.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_catalogcategory_buffer',
                          columns=('source_id', 'parent_id', 'name', 'name_ukr', 'name_en'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_catalogcategory p
            SET               
                parent_id = b.parent_id,
                name = b.name,
                name_ukr = b.name_ukr,
                name_en = b.name_en,             
            FROM shop_catalogcategory_buffer b
            WHERE p.source_id = b.source_id;'''

        cur.execute(copy_sql)
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
            name character varying(250)
            group character varying(250)
            title character varying(250));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/offers.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_offer_buffer',
                          columns=('source_id', 'name', 'group', 'title'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_offer o
            SET               
                name = b.name,
                group = b.group,
                title = b.title,             
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
            category_id character varying(300),
            brand_id character varying(300),
            offer_id character varying(300),
            code character varying(300),
            name character varying(500),
            name_ukr character varying(500),
            name_en character varying(500),
            comment character varying(500),
            comment_ukr character varying(500),
            comment_en character varying(500),
            article character varying(300),
            specification character varying(300),
            ABC character varying(300),
            price_category character varying(300),
            advanced_description text,
            weight numeric(15,3),
            pack_qty integer,
            product_type integer,
            create_date timestamp with time zone,
            income_date timestamp with time zone);'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/products.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_product_buffer',
                          columns=(
                          'source_id', 'category_id', 'brand_id', 'offer_id', 'code', 'name', 'name_ukr', 'name_en',
                          'comment', 'comment_ukr', 'comment_en', 'article', 'specification', 'ABC', 'price_category',
                          'advanced_description', 'weight', 'pack_qty', 'product_type', 'create_date',
                          'income_date'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_product p
            SET               
                category_id = b.category_id,
                brand_id = b.brand_id,
                offer_id = b.offer_id,
                code = b.code,
                name = b.name,
                name_ukr = b.name_ukr,
                name_en = b.name_en,
                comment = b.comment,
                comment_ukr = b.comment_ukr,
                comment_en = b.comment_en,
                article = b.article,
                specification = b.specification,
                ABC = b.ABC,
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
        self.conn.close()

    def load_customer_points(self):
        customer_points = self.client.service.GetData('customer_points')
        data = base64.b64decode(customer_points)
        file = open('cache/customer_points.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_customerpoint_buffer (
            customer_source_id character varying(300),        
            source_id character varying(300),
            name character varying(300)
            add character varying(300));'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_points.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_customerpoint_buffer',
                          columns=('customer_source_id', 'source_id', 'name', 'add'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_customerpoint c
            SET               
                name = b.name,
                add = b.add                           
            FROM shop_customerpoint_buffer b
            WHERE c.source_id = b.source_id;'''

        cur.execute(copy_sql)
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
            customer_source_id character varying(300), 
            currency_source_id character varying(300), 
            price_type_source_id character varying(300), 
            code character varying(300), 
            name character varying(300),
            number character varying(300),
            discount character varying(300),
            is_status character varying(300),
            is_active character varying(300) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_agreements.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_customeragreement_buffer',
                          columns=('source_id', 'customer_source_id', 'currency_source_id', 'price_type_source_id',
                                   'code', 'name', 'number', 'discount', 'is_status', 'is_active'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_customeragreement c
            SET
                customer_source_id = b.customer_source_id,
                currency_source_id = b.currency_source_id,
                price_type_source_id = b.price_type_source_id,
                code = b.code,
                name = b.name,               
                number = b.number,
                discount = b.discount,
                is_status = b.is_status,
                is_active = b.is_active                                   
            FROM shop_customerpoint_buffer b
            WHERE c.source_id = b.source_id;'''

        cur.execute(copy_sql)
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
            customer_source character varying(300),
            agreement_source character varying(300), 
            currency_source character varying(300), 
            balance numeric(15,2), 
            past_due numeric(15,2) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/balances.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_balance_buffer',
                          columns=('customer_source', 'agreement_source', 'currency_source', 'balance',
                                   'past_due'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_customeragreement c
            SET
                agreement_source = b.agreement_source,
                currency_source = b.currency_source, 
                balance = b.balance, 
                past_due = b.past_due            
            FROM shop_customeragreement_buffer b
            WHERE c.customer_source = b.customer_source;'''

        cur.execute(copy_sql)
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
            criteria_source_id character varying(300),
            customer_source_id character varying(300), 
            agreement_source_id character varying(300), 
            price_type_source_id character varying(300), 
            criteria_type character varying(300), 
            discount numeric(15, 2) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/customer_discounts.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_customerdiscount_buffer',
                          columns=('criteria_source_id', 'customer_source_id', 'agreement_source_id',
                                   'price_type_source_id', 'criteria_type', 'discount'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_customerdiscount c
            SET
                criteria_source_id = b.criteria_source_id,
                agreement_source_id = b.agreement_source_id, 
                price_type_source_id = b.price_type_source_id, 
                criteria_type = b.criteria_type,
                discount = b.discount            
            FROM shop_customerdiscount_buffer b
            WHERE c.customer_source_id = b.customer_source_id;'''

        cur.execute(copy_sql)
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
                agreement_source character varying(300),
                order_source character varying(300), 
                credit numeric(15, 2), 
                debit numeric(15, 2), 
                balance numeric(15, 2) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/dropshipping_wallet.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_dropshippingwallet_buffer',
                          columns=('agreement_source', 'order_source', 'credit', 'debit', 'balance'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_dropshippingwallet d
                SET
                    agreement_source = b.agreement_source,
                    credit = b.price_type_source_id, 
                    debit = b.debit,
                    balance = b.balance            
                FROM shop_dropshippingwallet_buffer b
                WHERE d.order_source = b.order_source;'''

        cur.execute(copy_sql)
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
                product_source_id character varying(300),
                price_type_source_id character varying(300), 
                currency_source_id character varying(300), 
                price numeric(15, 2) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/prices.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_price_buffer',
                          columns=('product_source_id', 'price_type_source_id', 'currency_source_id', 'price'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_price p
                SET
                    price_type_source_id = b.price_type_source_id,
                    currency_source_id = b.currency_source_id, 
                    price = b.price          
                FROM shop_price_buffer b
                WHERE p.product_source_id = b.product_source_id;'''

        cur.execute(copy_sql)
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
                product_source character varying(300),
                customer_source character varying(300), 
                qty integer, 
                date timestamp with time zone );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/sales.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_sale_buffer',
                          columns=('product_source', 'customer_source', 'qty', 'date'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_sale s
                SET
                    customer_source = b.customer_source,
                    qty = b.qty, 
                    date = b.date          
                FROM shop_sale_buffer b
                WHERE s.product_source = b.product_source;'''

        cur.execute(copy_sql)
        self.conn.commit()
        self.conn.close()

    def load_sale_tasks(self):
        sale_tasks = self.client.service.GetData('sale_tasks')
        data = base64.b64decode(sale_tasks)
        file = open('cache/sale_tasks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE shop_sale_buffer (
                product_source character varying(300),
                customer_source character varying(300), 
                qty integer );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/sale_tasks.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_saletask_buffer',
                          columns=('product_source', 'customer_source', 'qty'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_saletask s
                SET
                    customer_source = b.customer_source,
                    qty = b.qty                             
                FROM shop_saletask_buffer b
                WHERE s.product_source = b.product_source;'''

        cur.execute(copy_sql)
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
                product_source_id character varying(300),
                stock_name character varying(300), 
                amount_total integer 
                amount_account integer );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/stocks.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_stock_buffer',
                          columns=('product_source_id', 'stock_name', 'amount_total', 'amount_account'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_stock s
                SET
                    stock_name = b.stock_name,
                    amount_total = b.amount_total, 
                    amount_account = b.amount_account                             
                FROM shop_stock_buffer b
                WHERE s.product_source_id = b.product_source_id;'''

        cur.execute(copy_sql)
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
                product_source_id character varying(300),
                sale_policy character varying(300), 
                amount_account integer );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/deficit.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_deficitreserve_buffer',
                          columns=('product_source_id', 'sale_policy', 'amount_account'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_deficitreserve d
                SET
                    sale_policy = b.sale_policy,
                    amount_account = b.amount_account                         
                FROM shop_deficitreserve_buffer b
                WHERE d.product_source_id = b.product_source_id;'''

        cur.execute(copy_sql)
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
                product_source_id character varying(300),
                property character varying(300), 
                value text );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/description.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_productdescription_buffer',
                          columns=('product_source_id', 'property', 'value'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_productdescription p
                SET
                    property = b.property,
                    value = b.value                         
                FROM shop_productdescription_buffer b
                WHERE p.product_source_id = b.product_source_id;'''

        cur.execute(copy_sql)
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
                product_source_id character varying(300),
                vehicle character varying(300),
                modification character varying(300), 
                engine character varying(300), 
                year character varying(300) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/applicability.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_productapplicability_buffer',
                          columns=('product_source_id', 'vehicle', 'modification', 'engine', 'year'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_productapplicability p
                SET
                    vehicle = b.vehicle,
                    modification = b.modification,
                    engine = b.engine,
                    year = b.year                         
                FROM shop_productapplicability_buffer b
                WHERE p.product_source_id = b.product_source_id;'''

        cur.execute(copy_sql)
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
                product_source_id character varying(300),
                brand_name character varying(300),                
                article_nr character varying(300) );'''

        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/cross.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'shop_cross_buffer',
                          columns=('product_source_id', 'brand_name', 'article_nr'), sep='|')

        self.conn.commit()

        copy_sql = '''UPDATE shop_cross p
                SET
                    brand_name = b.brand_name,
                    article_nr = b.article_nr                       
                FROM shop_cross_buffer b
                WHERE p.product_source_id = b.product_source_id;'''

        cur.execute(copy_sql)
        self.conn.commit()
        self.conn.close()

    def load_orders(self):
        orders = self.client.service.GetData('orders')
        data = base64.b64decode(orders)
        file = open('cache/orders.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_order_items(self):
        order_items = self.client.service.GetData('order_items')
        data = base64.b64decode(order_items)
        file = open('cache/order_items.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_declaration_numbers(self):
        declaration_numbers = self.client.service.GetData('declaration_numbers')
        data = base64.b64decode(declaration_numbers)
        file = open('cache/declaration_numbers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()


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
# loadData.load_customer_discounts()
# loadData.load_balances()
# loadData.load_dropshipping_wallet()
# loadData.load_sales()
# loadData.load_sale_tasks()
# loadData.load_description()
# loadData.load_applicability()
# loadData.load_prices()
# loadData.load_cross()
# loadData.load_stocks()
# loadData.load_deficit()
# loadData.load_orders()
# loadData.load_order_items()
# loadData.load_declaration_numbers()
