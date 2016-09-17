from rest_framework import serializers

from .models import User
from accounts.models import (
    Owner,
    Employee,
    Customer,
    Supplier
)
from business.models import Business
from djangae.contrib.gauth.datastore.models import Group
from django.contrib.auth.models import Permission

class AccountsBusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('id', 'name')

class UserOwnerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('id', 'user', 'business')

class UserEmployeeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = ('id', 'user', 'business')

class UserCustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'business')

class UserSupplierSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    business = AccountsBusinessSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'business')

class UserSerializer(serializers.ModelSerializer):
    is_owner = serializers.BooleanField(default=False)
    is_employee = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    is_supplier = serializers.BooleanField(default=False)
    owner = UserOwnerSerializer(read_only=True)
    employee = UserEmployeeSerializer(read_only=True)
    customer = UserCustomerSerializer(read_only=True)
    supplier = UserSupplierSerializer(read_only=True)
    # business = serializers.SerializerMethodField()
    #
    # @staticmethod
    # def business_query(query_kargs):
    #     return [{'id':bs.pk, 'name':bs.name} for bs in Business.objects.filter(**query_kargs)]
    #
    # def get_business(self, user):
    #     if user.is_owner:
    #         return self.business_query({'owner':user.owner})
    #     if user.is_employee:
    #         return self.business_query({'employees__contains': user.employee})
    #     if user.is_customer:
    #         return self.business_query({'customers__contains': user.customer})
    #     if user.is_supplier:
    #         return self.business_query({'suppliers__contains': user.supplier})
    #     else:
    #         return None

    class Meta:
        model = User
        fields = (
                  'id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'is_owner',
                  'is_employee',
                  'is_customer',
                  'is_supplier',
                  'owner',
                  'employee',
                  'customer',
                  'supplier',
                  'password',
                  'url'
                  )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    username=validated_data['username'],
                    email=validated_data['email'],
                    is_owner=validated_data['is_owner'],
                    is_employee=validated_data['is_employee'],
                    is_customer=validated_data['is_customer'],
                    is_supplier=validated_data['is_supplier'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GroupSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all())

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions', 'url')
