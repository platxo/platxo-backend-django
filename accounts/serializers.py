from rest_framework import serializers
from .models import Owner, Employed, Customer, Supplier


class OwnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Owner
        fields = ('id', 'user', 'business', 'created', 'updated', 'url')


class EmployedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employed
        fields = ('id', 'user', 'created', 'updated', 'url')


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'user', 'created', 'updated', 'url')

class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'created', 'updated', 'url')
