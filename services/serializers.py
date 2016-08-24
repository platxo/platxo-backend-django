from rest_framework import serializers

from .models import Service, ServiceCategory, ServiceType


class ServiceCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ServiceCategory
        fields = ('id', 'name', 'created', 'updated', 'url')


class ServiceTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = ServiceType
        fields = ('id', 'service_category', 'name', 'created', 'updated', 'url')


class ServiceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Service
        fields = ('id', 'service_category', 'service_type', 'name', 'description', 'supplier', 'price', 'image', 'picture', 'created', 'updated', 'url')
