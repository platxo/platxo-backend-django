from rest_framework import serializers
from .models import Owner, Employee, Customer, Supplier
from business.models import Business
from customers.models import Point

class CustomerPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = Point
        fields = ('id', 'business', 'balance')

class AccountsBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('id', 'name')


class OwnerSerializer(serializers.ModelSerializer):
    business = AccountsBusinessSerializer(many=True, read_only=True)
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        return ({'owner_name':obj.user.username})

    class Meta:
        model = Owner
        fields = ('id', 'user', 'business', 'extra', 'created', 'updated', 'url')


class EmployeeSerializer(serializers.ModelSerializer):
    business = AccountsBusinessSerializer(many=True, read_only=True)
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        return ({'employee_name':obj.user.username})

    class Meta:
        model = Employee
        fields = ('id', 'user', 'business', 'extra', 'created', 'updated', 'url')


class CustomerSerializer(serializers.ModelSerializer):
    business = AccountsBusinessSerializer(many=True, read_only=True)
    points = CustomerPointSerializer(many=True, read_only=True)
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        return ({'customer_name':obj.user.username})

    class Meta:
        model = Customer
        fields = ('id', 'user', 'business', 'points', 'extra', 'created', 'updated', 'url')


class SupplierSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)
    extra = serializers.SerializerMethodField()

    def get_extra(self, obj):
        return ({'supplier_name':obj.user.username})

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'business', 'extra', 'created', 'updated', 'url')
