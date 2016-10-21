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
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        try:
            location_name = obj.location.name
        except Exception:
            location_name = None
        return ({'location_name': location_name})

    class Meta:
        model = Section
        fields = ('id', 'business', 'employee', 'location', 'name', 'extra', 'created', 'updated', 'url')

class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')


class ProductTypeSerializer(serializers.ModelSerializer):
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        try:
            product_category_name = obj.product_category.name
        except Exception:
            product_category_name = None
        return ({'product_category_name': product_category_name})

    class Meta:
        model = ProductType
        fields = ('id', 'business', 'employee', 'product_category', 'name', 'extra', 'created', 'updated', 'url')


class ProductSerializer(serializers.ModelSerializer):
    picture = Base64ImageField(required=False, allow_null=True, write_only=True)
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        try:
            tax_name = obj.tax.name
        except Exception:
            tax_name = None
        try:
            tax_rate = obj.tax.rate
        except Exception:
            tax_rate = None
        try:
            product_category_name = obj.product_category.name
        except Exception:
            product_category_name = None
        try:
            product_type_name = obj.product_type.name
        except Exception:
            product_type_name = None
        try:
            location_name = obj.location.name
        except Exception:
            location_name = None
        try:
            section_name = obj.section.name
        except Exception:
            section_name = None
        try:
            brand_name = obj.brand.name
        except Exception:
            brand_name = None
        try:
            code_url = obj.code.qrcode.url
        except Exception:
            code_url = None
        try:
            picture_url = obj.picture.url
        except Exception:
            picture_url = None
        return ({'tax_name': tax_name,
                 'tax_rate': tax_rate,
                 'product_category_name': product_category_name,
                 'product_type_name': product_type_name,
                 'location_name': location_name,
                 'section_name': section_name,
                 'brand_name': brand_name,
                 'code_url': code_url,
                 'picture_url': picture_url})

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
                  'name',
                  'description',
                  'supply_price',
                  'retail_price',
                  'tax',
                  'inventory',
                  'stock',
                  'quantity',
                  'image',
                  'picture',
                  'extra',
                  'created',
                  'updated',
                  'url')
