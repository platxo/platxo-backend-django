from django.shortcuts import render
from rest_framework import viewsets

from business.models import Business
from .models import ServiceCategory, ServiceType, Service
from .serializers import ServiceCategorySerializer, ServiceTypeSerializer, ServiceSerializer


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employed:
            business_query = Business.objects.filter(employees__contains=user.employed)
        else:
            business_query = list()

        return self.queryset.filter(business__in=business_query)


class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employed:
            business_query = Business.objects.filter(employees__contains=user.employed)
        else:
            business_query = list()

        return self.queryset.filter(business__in=business_query)


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employed:
            business_query = Business.objects.filter(employees__contains=user.employed)
        else:
            business_query = list()

        return self.queryset.filter(business__in=business_query)
