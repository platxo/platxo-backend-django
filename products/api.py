from rest_framework import serializers, viewsets
from .models import Product, ProductCategory, ProductType

# Serializers

class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'name', 'created', 'updated', 'url')


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):
    #category = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = ProductType
        fields = ('id', 'product_category', 'name', 'created', 'updated', 'url')


class ProductSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Product
        fields = ('id', 'product_category', 'product_type', 'name', 'description', 'supplier', 'location', 'price', 'quantity', 'stock', 'image', 'picture', 'created', 'updated', 'url')


# Viewsets

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
