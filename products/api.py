from rest_framework import serializers, viewsets
from .models import Product, Category, Type

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


class ProductSerializer(serializers.HyperlinkedModelSerializer):


    class Meta:
        model = Product
        fields = ('id', 'category', 'type', 'name', 'description', 'supplier', 'location', 'price', 'quantity', 'stock', 'image', 'picture', 'created', 'updated', 'url')


# Viewsets

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
