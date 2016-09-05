from rest_framework import serializers
from .models import Owner, Employed, Customer, Supplier

class OwnerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Owner
        fields = ('id', 'user', 'created', 'updated', 'url')


class EmployedSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employed
        fields = ('id', 'user', 'created', 'updated', 'url')


class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        fields = ('id', 'user', 'created', 'updated', 'url')

class SupplierSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Supplier
        fields = ('id', 'user', 'created', 'updated', 'url')
