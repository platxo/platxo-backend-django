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
        return ({'tax_name':obj.tax.name,
                 'tax_rate':obj.tax.rate,
                 'product_category_name':obj.product_category.name,
                 'product_type_name':obj.product_type.name,
                 'location_name':obj.location.name,
                 'section_name':obj.section.name})

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
