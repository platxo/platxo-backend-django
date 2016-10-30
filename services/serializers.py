from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Service, ServiceCategory, ServiceType


class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategory
        fields = ('id',
                  'business',
                  'employee',
                  'name',
                  'description',
                  'created',
                  'updated',
                  'url')


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('id',
                  'business',
                  'employee',
                  'service_category',
                  'service_category_name',
                  'name',
                  'description',
                  'created',
                  'updated',
                  'url')


class ServiceSerializer(serializers.ModelSerializer):
    picture = Base64ImageField(required=False, allow_null=True, write_only=True)
    service_category_name = serializers.CharField(read_only=True)
    service_type_name = serializers.CharField(read_only=True)
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
        model = Service
        fields = ('id',
                  'business',
                  'employee',
                  'service_category',
                  'service_type',
                  'tax',
                  'service_category_name',
                  'service_type_name',
                  'tax_name',
                  'tax_rate',
                  'name',
                  'description',
                  'price',
                  'image',
                  'picture',
                  'picture_url',
                  'created',
                  'updated',
                  'url')
