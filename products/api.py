from rest_framework import serializers, viewsets
from .models import Product

# Serializers

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'stock', 'category', 'type', 'name', 'price', 'quantity', 'picture', 'url')


# Viewsets

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializers_class = ProductSerializer
