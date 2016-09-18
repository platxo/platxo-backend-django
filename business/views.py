from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import filters

from .models import Business, Data, Information, Knowledge
from .serializers import BusinessSerializer, DataSerializer, InformationSerializer, KnowledgeSerializer
from .filters import DataFilter


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_owner and user.owner:
    #         owner_query = user.owner
    #     else:
    #         owner_query = None
    #     return self.queryset.filter(owner=owner_query)

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner:
            return self.queryset.filter(owner=user.owner)
        elif user.is_employee and user.employee:
            return self.queryset.filter(employees__contains=user.employee)
        else:
            return None




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
