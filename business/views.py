from django.shortcuts import render
from rest_framework import viewsets

from .models import Data, Information, Knowledge
from .serializers import DataSerializer, InformationSerializer, KnowledgeSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer
