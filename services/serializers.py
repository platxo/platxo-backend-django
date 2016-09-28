from rest_framework import serializers

from .models import Service, ServiceCategory, ServiceType


class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategory
        fields = ('id', 'business', 'employee', 'name', 'created', 'updated', 'url')


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('id', 'business', 'employee', 'service_category', 'name', 'created', 'updated', 'url')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id',
                  'business',
                  'employee',
                  'tax',
                  'service_category',
                  'service_type',
                  'name',
                  'description',
                  'price',
                  'image',
                  'picture',
                  'created',
                  'updated',
                  'url'
                  )
