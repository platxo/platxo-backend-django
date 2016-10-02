from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters

from .models import Business, Tax, Data, Information, Knowledge
from .serializers import BusinessSerializer, TaxSerializer, DataSerializer, InformationSerializer, KnowledgeSerializer
from .filters import DataFilter


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner:
            return self.queryset.filter(owner=user.owner)
        if user.is_employee and user.employee:
            return self.queryset.filter(employees__contains=user.employee)
        if user.is_customer and user.customer:
            return self.queryset.filter(customers__contains=user.customer)
        if user.is_supplier and user.supplier:
            return self.queryset.filter(suppliers__contains=user.supplier)
        if user.is_owner and user.employee:
            return self.queryset.filter(employees__contains=user.employee)
        if user.is_owner and user.customer:
            return self.queryset.filter(customers__contains=user.customer)
        if user.is_owner and user.supplier:
            return self.queryset.filter(suppliers__contains=user.supplier)
        else:
            return None


class TaxViewSet(viewsets.ModelViewSet):
    queryset = Tax.objects.all()
    serializer_class = TaxSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    #filter_backends = (filters.DjangoFilterBackend,)
    # filter_class = DataFilter
    #filter_fields = ('business',)

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)


class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)
