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
        Validate each product / service condition is applicable
        """

        if data.get('products'):
            try:
                products_id = [product['id'] for product in data.get('products')]
            except KeyError as e:
                print e.message
                raise serializers.ValidationError({'product': 'Missing id.'})

        products = Product.objects.filter(pk__in=products_id)

        if len(products_id) != len(products):
            raise serializers.ValidationError({'product': 'Duplicated or missing id.'})
        print len(products)
        return data
