from django.shortcuts import render
from rest_framework import viewsets

from .models import Business, Data, Information, Knowledge
from .serializers import BusinessSerializer, DataSerializer, InformationSerializer, KnowledgeSerializer

import django_filters

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class DataFilter(django_filters.FilterSet):

    class Meta:
        model = Data
        fields = ['business',]


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    filter_class = DataFilter


class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer
