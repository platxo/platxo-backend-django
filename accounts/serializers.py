from rest_framework import serializers
from .models import Owner, Employee, Customer, Supplier
from business.models import Business

class AccountsBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('id', 'name')


class OwnerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class EmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class SupplierSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')
