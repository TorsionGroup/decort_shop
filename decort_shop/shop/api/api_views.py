from rest_framework.generics import ListAPIView

from .serializers import BrandSerializer
from ..models import *


class BrandListAPIView(ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

