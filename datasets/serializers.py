from rest_framework import serializers
from .models import Table


class PreviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = [
            'columns',
            'sample',
            'schema',
        ]
