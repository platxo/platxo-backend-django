from django.shortcuts import render
from rest_framework import viewsets

from .serializers import OwnerSerializer, EmployedSerializer, CustomerSerializer
from.models import Owner, Employed, Customer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class EmployedViewSet(viewsets.ModelViewSet):
    queryset = Employed.objects.all()
    serializer_class = EmployedSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
