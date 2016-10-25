from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Product, ProductCategory, ProductType, Location, Section, Brand

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')

class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Section
        fields = ('id', 'business', 'employee', 'location', 'location_name', 'name', 'created', 'updated', 'url')

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')


class ProductTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductType
        fields = ('id', 'business', 'employee', 'product_category', 'product_category_name', 'name', 'created', 'updated', 'url')


class ProductSerializer(serializers.ModelSerializer):
    picture = Base64ImageField(required=False, allow_null=True, write_only=True)
    product_category_name = serializers.CharField(read_only=True)
    product_type_name = serializers.CharField(read_only=True)
    location_name = serializers.CharField(read_only=True)
    section_name = serializers.CharField(read_only=True)
    brand_name = serializers.CharField(read_only=True)
    tax_name = serializers.CharField(read_only=True)
    tax_rate = serializers.IntegerField(read_only=True)
    picture_url = serializers.SerializerMethodField()

    def get_picture_url(self, obj):
        try:
            picture_url = obj.picture.url
        except Exception:
            picture_url = None
        return picture_url

    class Meta:
        model = Product
        fields = ('id',
                  'business',
                  'employee',
                  'supplier',
                  'product_category',
                  'product_type',
                  'location',
                  'section',
                  'brand',
                  'tax',
                  'product_category_name',
                  'product_type_name',
                  'location_name',
                  'section_name',
                  'brand_name',
                  'tax_name',
                  'tax_rate',
                  'name',
                  'description',
                  'supply_price',
                  'retail_price',
                  'inventory',
                  'stock',
                  'quantity',
                  'image',
                  'picture',
                  'picture_url',
                  'created',
                  'updated',
                  'url')
