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
            product_type_name = obj.product_category.name
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
            code_url = obj.code.qrcode.url
        except Exception:
            code_url = None
        return ({'tax_name': tax_name,
                 'tax_rate': tax_rate,
                 'product_category_name': product_category_name,
                 'product_type_name': product_type_name,
                 'location_name': location_name,
                 'section_name': section_name,
                 'code_url': code_url})

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
                  'name',
                  'description',
                  'supply_price',
                  'retail_price',
                  'tax',
                  'inventory',
                  'quantity',
                  'image',
                  'picture',
                  'extra',
                  'created',
                  'updated',
                  'url')
