from rest_framework import serializers
from .models import Owner, Employee, Customer, Supplier


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')
