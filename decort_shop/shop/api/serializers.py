from rest_framework import serializers

from ..models import *


class BrandSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    source_id = serializers.CharField()

    class Meta:
        model = Brand
        fields = [
            'name', 'source_id'
        ]