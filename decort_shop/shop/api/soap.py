import base64
import json
import requests
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.cache import SqliteCache


class LoadData:
    def __init__(self, user='Robot', password='Robot'):
        self.user = user.encode('utf-8')
        self.password = password.encode('utf-8')

        session = Session()
        session.auth = HTTPBasicAuth(self.user, self.password)
        transport = Transport(session=session)
        self.client = Client('http://192.168.75.115:8005/live/ws/b2b?wsdl', transport=transport)

    def load_brand(self):
        brands = self.client.service.GetData('brands')
        data = base64.b64decode(brands)
        return data

print(load_brand)


# session = Session()
# session.auth = HTTPBasicAuth('Robot', 'Robot')
# client = Client('http://192.168.75.115:8005/live/ws/b2b?wsdl', transport=Transport(session=session))
# brands = client.service.GetData('brands')
# data = base64.b64decode(brands)
# print(data)
