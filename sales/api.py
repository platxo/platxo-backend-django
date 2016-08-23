from rest_framework import serializers, viewsets

from .models import Sale
from products.models import Product
from services.models import  Service
# Serializers


class SaleSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Product.objects.all(),
        view_name='product-detail'
    )

    services = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Service.objects.all(),
        view_name='service-detail'
        )

    class Meta:
        model = Sale
        fields = ('id', 'customer', 'products', 'services', 'created', 'updated', 'url')

# Viewsets

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
