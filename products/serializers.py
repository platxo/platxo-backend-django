from rest_framework import serializers

from .models import Product, ProductCategory, ProductType, Location, Section


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('id', 'business', 'employee', 'location', 'name', 'created', 'updated', 'url')

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
        fields = ('id',
                  'business',
                  'employee',
                  'tax',
                  'supplier',
                  'product_category',
                  'product_type',
                  'location',
                  'section',
                  'name',
                  'description',
                  'supply_price',
                  'retail_price',
                  'tax',
                  'inventory',
                  'quantity',
                  'image',
                  'picture',
                  'created',
                  'updated',
                  'url'
                  )
