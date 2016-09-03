from rest_framework import serializers

from .models import Product, ProductCategory, ProductType

class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'user', 'name', 'created', 'updated', 'url')


class ProductTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ProductType
        fields = ('id', 'user', 'product_category', 'name', 'created', 'updated', 'url')


class ProductSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'user', 'product_category', 'product_type', 'name', 'description', 'supplier', 'location', 'price', 'quantity', 'stock', 'image', 'picture', 'created', 'updated', 'url')
