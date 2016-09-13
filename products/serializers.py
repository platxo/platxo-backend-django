from rest_framework import serializers

from .models import Product, ProductCategory, ProductType


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ('id', 'business', 'employee', 'product_category', 'name', 'created', 'updated', 'url')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'business', 'employee', 'product_category', 'product_type', 'name', 'description', 'supplier', 'location', 'price', 'quantity', 'stock', 'image', 'picture', 'created', 'updated', 'url')
