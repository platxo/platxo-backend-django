from rest_framework import serializers, viewsets
from .models import Sale

# Serializers


class SaleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sale
        fields = ('id', 'customer', 'product', 'created', 'updated', 'url')

# Viewsets

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer