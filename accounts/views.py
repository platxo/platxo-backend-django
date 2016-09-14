from django.shortcuts import render
from rest_framework import viewsets

from .serializers import OwnerSerializer, EmployeeSerializer, CustomerSerializer, SupplierSerializer
from.models import Owner, Employee, Customer, Supplier

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_owner and user.owner.business:
            business_query = user.owner.business.all()
        elif user.is_employee:
            business_query = Business.objects.filter(employees__contains=user.employee)
        else:
            business_query = list()
        return self.queryset.filter(business__in=business_query)
