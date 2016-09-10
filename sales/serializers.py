from rest_framework import serializers

from sales.validators import OneProductOrService, UserInBusiness
from .models import Sale, PurchaseOrder
from products.models import Product
from services.models import Service


class SaleSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())
    services = serializers.PrimaryKeyRelatedField(many=True, queryset=Service.objects.all())

    class Meta:
        model = Sale
        fields = ('id', 'business', 'employed', 'customer', 'products', 'services', 'total', 'created', 'updated', 'url')


class OrderRequestSerializer(serializers.ModelSerializer):
    products = serializers.ListField(required=False)
    services = serializers.ListField(required=False)

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'customer', 'employee', 'business', 'payment_method', 'products', 'services')
        validators = [OneProductOrService(),
                      UserInBusiness(field='employee'),
                      UserInBusiness(field='customer', anonymous=True)]

    def validate(self, data):
        """
        Validate that employee and customer belongs to the business.

        Ensure at least the products or service comes.
        """

        maped_products = []

        return data
