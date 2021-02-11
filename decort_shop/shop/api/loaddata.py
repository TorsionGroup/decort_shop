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

    def load_product_price_categories(self):
        product_price_categories = self.client.service.GetData('product_price_categories')
        data = base64.b64decode(product_price_categories)
        file = open('cache/product_price_categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_categories(self):
        categories = self.client.service.GetData('categories')
        data = base64.b64decode(categories)
        file = open('cache/categories.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_customer_points(self):
        customer_points = self.client.service.GetData('customer_points')
        data = base64.b64decode(customer_points)
        file = open('cache/customer_points.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_customer_agreements(self):
        customer_agreements = self.client.service.GetData('customer_agreements')
        data = base64.b64decode(customer_agreements)
        file = open('cache/customer_agreements.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_balances(self):
        balances = self.client.service.GetData('balances')
        data = base64.b64decode(balances)
        file = open('cache/balances.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_customer_discounts(self):
        customer_discounts = self.client.service.GetData('customer_discounts')
        data = base64.b64decode(customer_discounts)
        file = open('cache/customer_discounts.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_dropshipping_wallet(self):
        dropshipping_wallet = self.client.service.GetData('dropshipping_wallet')
        data = base64.b64decode(dropshipping_wallet)
        file = open('cache/dropshipping_wallet.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_sales(self):
        sales = self.client.service.GetData('sales')
        data = base64.b64decode(sales)
        file = open('cache/sales.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_sale_tasks(self):
        sale_tasks = self.client.service.GetData('sale_tasks')
        data = base64.b64decode(sale_tasks)
        file = open('cache/sale_tasks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_offers(self):
        offers = self.client.service.GetData('offers')
        data = base64.b64decode(offers)
        file = open('cache/offers.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_products(self):
        products = self.client.service.GetData('products')
        data = base64.b64decode(products)
        file = open('cache/products.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_description(self):
        description = self.client.service.GetData('description')
        data = base64.b64decode(description)
        file = open('cache/description.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_applicability(self):
        applicability = self.client.service.GetData('applicability')
        data = base64.b64decode(applicability)
        file = open('cache/applicability.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_prices(self):
        prices = self.client.service.GetData('prices')
        data = base64.b64decode(prices)
        file = open('cache/prices.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_cross(self):
        cross = self.client.service.GetData('cross')
        data = base64.b64decode(cross)
        file = open('cache/cross.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_stocks(self):
        stocks = self.client.service.GetData('stocks')
        data = base64.b64decode(stocks)
        file = open('cache/stocks.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

    def load_deficit(self):
        deficit = self.client.service.GetData('deficit')
        data = base64.b64decode(deficit)
        file = open('cache/deficit.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

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
# loadData.load_product_price_categories()
# loadData.load_categories()
# loadData.load_customer_points()
# loadData.load_customer_agreements()
# loadData.load_customer_discounts()
# loadData.load_balances()
# loadData.load_dropshipping_wallet()
# loadData.load_sales()
# loadData.load_sale_tasks()
# loadData.load_offers()
# loadData.load_products()
# loadData.load_description()
# loadData.load_applicability()
# loadData.load_prices()
# loadData.load_cross()
# loadData.load_stocks()
# loadData.load_deficit()
# loadData.load_orders()
# loadData.load_order_items()
# loadData.load_declaration_numbers()
