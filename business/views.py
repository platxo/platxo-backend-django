from django.shortcuts import render
from rest_framework import viewsets

from .models import Business, Data, Information, Knowledge
from .serializers import BusinessSerializer, DataSerializer, InformationSerializer, KnowledgeSerializer


class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer

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
