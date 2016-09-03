from django.shortcuts import render
from rest_framework import viewsets

from .models import Business, Data, Information, Knowledge
from .serializers import BusinessSerializer, DataSerializer, InformationSerializer, KnowledgeSerializer

class BusinessViewSet(viewsets.ModelViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer


class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

    def get_queryset(self):
        return self.request.user.datas.all()


class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer

    def get_queryset(self):
        return self.request.user.informations.all()


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer

    def get_queryset(self):
        return self.request.user.knowledges.all()
