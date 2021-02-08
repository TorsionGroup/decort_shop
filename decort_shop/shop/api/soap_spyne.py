from spyne.application import Application
from spyne.decorator import rpc, srpc
from spyne.service import ServiceBase
from spyne.model.complex import Iterable
from spyne.model.primitive import UnsignedInteger, String, Integer, Unicode
from lxml import etree
from spyne.protocol.soap import Soap11
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
from spyne.server.django import DjangoApplication
from django.views.decorators.csrf import csrf_exempt


class LoadData(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def load_brand(ctx, name, times):
        for i in range(times):
            yield 'Hello, %s' % name
application = Application([HelloWorldService],
    tns='spyne.examples.hello',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=JsonDocument()
)

hello_app = csrf_exempt(DjangoApplication(application))
