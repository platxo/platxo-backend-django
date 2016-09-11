from rest_framework import serializers

from .models import Sale
from products.models import Product
from services.models import  Service


class SaleSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    services = serializers.PrimaryKeyRelatedField(many=True, queryset=Service.objects.all())

    class Meta:
        model = Sale
        fields = ('id', 'business', 'employee', 'customer', 'products', 'services', 'total', 'created', 'updated', 'url')
