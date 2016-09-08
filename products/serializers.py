from rest_framework import serializers

from .models import Product, ProductCategory, ProductType

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'business', 'employed', 'name', 'created', 'updated', 'url')


class ProductTypeSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer()

    class Meta:
        model = ProductType
        fields = ('id', 'business', 'employed', 'product_category', 'name', 'created', 'updated', 'url')


class ProductSerializer(serializers.ModelSerializer):
    product_category = ProductCategorySerializer()
    product_type = ProductTypeSerializer()

    class Meta:
        model = Product
        fields = ('id', 'business', 'employed', 'product_category', 'product_type', 'name', 'description', 'supplier', 'location', 'price', 'quantity', 'stock', 'image', 'picture', 'created', 'updated', 'url')
