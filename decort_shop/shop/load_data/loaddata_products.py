import base64
import psycopg2
from zeep import Client, Settings
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport


class LoadDataProducts:
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
            article_nr character varying(300),
            search_nr character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/cross.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_cross_buffer',
                          columns=('product', 'brand', 'article_nr', 'search_nr'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_cross p
            SET
                brand = b.brand,
                article_nr = b.article_nr, 
                search_nr = b.search_nr                       
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

    def load_product_manufacturer_model(self):
        deficit = self.client.service.GetData('product_manufacturer_model')
        data = base64.b64decode(deficit)
        file = open('cache/product_manufacturer_model.csv', 'w', newline='', encoding='utf-8')
        file.write(str(data.decode('utf-8')))
        file.close()

        cur = self.conn.cursor()

        t_sql = '''CREATE TEMP TABLE products_productmanufacturermodel_buffer (
            product character varying(300),
            manufacturer_name character varying(300),
            model_name character varying(300),
            manufacturer_tecdoc_id character varying(300),                
            model_tecdoc_id character varying(300) );'''
        cur.execute(t_sql)
        self.conn.commit()

        with open('cache/product_manufacturer_model.csv', 'r', encoding='utf-8') as file:
            cur.copy_from(file, 'products_productmanufacturermodel_buffer',
                          columns=('product', 'manufacturer_name', 'model_name', 'manufacturer_tecdoc_id',
                                   'model_tecdoc_id'), sep='|')
        self.conn.commit()

        copy_sql = '''UPDATE products_productmanufacturermodel m
            SET
                manufacturer_name = b.manufacturer_name,
                model_name = b.model_name,
                manufacturer_tecdoc_id = b.manufacturer_tecdoc_id,
                model_tecdoc_id = b.model_tecdoc_id                       
            FROM products_productmanufacturermodel_buffer b
            WHERE m.product = b.product;'''
        cur.execute(copy_sql)
        self.conn.commit()

        upd_sql = '''UPDATE products_productmanufacturermodel m
            SET product_id_id = c.id                               
            FROM shop_product c
            WHERE m.product = c.source_id;'''
        cur.execute(upd_sql)
        self.conn.commit()

    # def load_product_images(self):
    #     product_images = self.client.service.GetData('product_images_hort')
    #     data = base64.b64decode(product_images)
    #     file = open('cache/product_images.csv', 'w', newline='', encoding='utf-8')
    #     file.write(str(data.decode('utf-8')))
    #     file.close()
    #
    #     cur = self.conn.cursor()
    #
    #     t_sql = '''CREATE TEMP TABLE hort_productimage_buffer (
    #                 source_product character varying(300),
    #                 image_url character varying(300) );'''
    #     cur.execute(t_sql)
    #     self.conn.commit()
    #
    #     with open('cache/product_images.csv', 'r', encoding='utf-8') as file:
    #         cur.copy_from(file, 'hort_productimage_buffer',
    #                       columns=('source_product', 'image_url'), sep='|')
    #     self.conn.commit()
    #
    #     ins_sql = '''INSERT INTO hort_productimage (source_product)
    #                     SELECT source_product FROM hort_productimage_buffer
    #                     WHERE source_product NOT IN (SELECT source_product FROM hort_productimage
    #                     WHERE source_product IS NOT NULL);'''
    #     cur.execute(ins_sql)
    #     self.conn.commit()
    #
    #     del_sql = '''DELETE FROM hort_productimage
    #                     WHERE source_product NOT IN (SELECT source_product FROM hort_productimage_buffer);'''
    #     cur.execute(del_sql)
    #     self.conn.commit()
    #
    #     copy_sql = '''UPDATE hort_productimage p
    #                 SET
    #                     image_url = b.image_url
    #                 FROM hort_productimage_buffer b
    #                 WHERE p.source_product = b.source_product;'''
    #     cur.execute(copy_sql)
    #     self.conn.commit()
    #
    #     upd_sql = '''UPDATE hort_productimage a
    #                 SET product_id = c.id
    #                 FROM hort_product c
    #                 WHERE a.source_product = c.source_id;'''
    #     cur.execute(upd_sql)
    #     self.conn.commit()


LoadDataProducts = LoadDataProducts()
LoadDataProducts.load_cross()
LoadDataProducts.load_description()
LoadDataProducts.load_applicability()
LoadDataProducts.load_product_price_categories()
LoadDataProducts.load_prices()
LoadDataProducts.load_stocks()
LoadDataProducts.load_deficit()
LoadDataProducts.load_product_manufacturer_model()
# LoadDataProducts.load_product_images()

print('Load Data Products')
