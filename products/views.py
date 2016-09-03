from django.shortcuts import render
from rest_framework import viewsets

from .models import ProductCategory, ProductType, Product
from .serializers import ProductCategorySerializer, ProductTypeSerializer, ProductSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        return self.request.user.product_categories.all()


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def get_queryset(self):
        return self.request.user.product_types.all()


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.products.all()
