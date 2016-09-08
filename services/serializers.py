from rest_framework import serializers

from .models import Service, ServiceCategory, ServiceType


class ServiceCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceCategory
        fields = ('id', 'business', 'employed', 'name', 'created', 'updated', 'url')


class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('id', 'business', 'employed', 'service_category', 'name', 'created', 'updated', 'url')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'business', 'employed', 'service_category', 'service_type', 'name', 'description', 'supplier', 'price', 'image', 'picture', 'created', 'updated', 'url')
