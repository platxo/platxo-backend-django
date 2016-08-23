from rest_framework import serializers, viewsets
from .models import Service, ServiceCategory, ServiceType

# Serializers

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


# Viewsets

class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
