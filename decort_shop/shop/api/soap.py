import base64
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.cache import SqliteCache


session = Session()
session.auth = HTTPBasicAuth('Robot', 'Robot')
client = Client('http://192.168.75.115:8005/live/ws/b2b?wsdl', transport=Transport(session=session))
brands = client.service.GetData('brands')
data = base64.b64decode(brands)
print(data)
