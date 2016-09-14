from rest_framework import serializers
from .models import Owner, Employee, Customer, Supplier


class OwnerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Owner
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Employee
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Customer
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class SupplierSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')
