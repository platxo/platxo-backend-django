from django.shortcuts import render
from rest_framework import viewsets

from business.models import Business
from .models import ProductCategory, ProductType, Product, Location, Section, Brand
from .serializers import (ProductCategorySerializer,
                          ProductTypeSerializer,
                          ProductSerializer,
                          LocationSerializer,
                          SectionSerializer,
                          BrandSerializer)


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)

class ProductCategoryViewSet(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
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
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
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
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)
