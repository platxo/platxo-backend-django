from django.shortcuts import render
from rest_framework import viewsets

from business.models import Business
from .models import ProductCategory, ProductType, Product
from .serializers import ProductCategorySerializer, ProductTypeSerializer, ProductSerializer


class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employed:
            business_query = Business.objects.filter(employees__contains=user.employed) #user.employed.business.all()
        else:
            business_query = list()

        return self.queryset.filter(business__in=business_query)


class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employed:
            business_query = Business.objects.filter(employees__contains=user.employed) #user.employed.business.all()
        else:
            business_query = list()

        return self.queryset.filter(business__in=business_query)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employed:
            business_query = Business.objects.filter(employees__contains=user.employed)
        else:
            business_query = list()

        return self.queryset.filter(business__in=business_query)

