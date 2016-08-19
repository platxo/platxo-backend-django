from rest_framework import serializers, viewsets
from .models import Service, Category, Type

# Serializers

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created', 'updated', 'url')


class TypeSerializer(serializers.HyperlinkedModelSerializer):
    #category = serializers.HyperlinkedIdentityField(view_name='category-detail')

    class Meta:
        model = Type
        fields = ('id', 'category', 'name', 'created', 'updated', 'url')


class ServiceSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Service
        fields = ('id', 'category', 'type', 'name', 'description', 'supplier', 'price', 'image', 'picture', 'created', 'updated', 'url')


# Viewsets

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
