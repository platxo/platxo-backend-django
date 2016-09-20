from copy import copy

from django.db.models import F
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
        fields = ('id', 'business', 'employee', 'customer', 'products', 'services', 'payment', 'total', 'created', 'updated', 'url')


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
                # Extract the id of the products to search them in database. And validate initial structure.
                products_id = [product['id'] for product in data.get('products')]
            except KeyError as e:
                print e.message
                raise serializers.ValidationError({'product': 'Missing id.'})

            # All products exists and belongs to the same business
            products = list(Product.objects.filter(pk__in=products_id, business=data.get('business').id))

            # If both don't match it's an error
            if len(products_id) != len(products):
                raise serializers.ValidationError({'product': 'Duplicated or missing id.'})

            mapped_products = list()
            # Validation of each product fields.
            for prod_id in data.get('products'):
                # Get the product with it's id
                product = next(prod for prod in products if prod.id == prod_id['id'])
                if not prod_id.get('qty'):
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Missing or invalid qty.'}})
                # There should be enough products in stock
                elif prod_id.get('qty') > product.quantity:
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Not enough products on stock.'}})
                # Discount must be between 0% and 100%
                elif not(0 <= prod_id.get("discount") <= 100):
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Discount not in range.'}})
                # Populate the product field
                product_object = copy(prod_id)
                product_object['products'] = product
                mapped_products.append(product_object)

            # Product now contains all information and save() van use this data.
            data['product'] = mapped_products

        return data

    def save(self, **kwargs):
        """
        Perform the order operation on each item.

        On products:

        Take the qty from stock and update the product object.
        Calculate the final item price and calculate the total price of all products.

        On service



        Finally add both products and services total price and save the order object

        :param kwargs:
        :return:
        """
        total_price = 0
        if self.validated_data.get('products'):
            for product in self.validated_data.get('product'):
                Product.objects.filter(pk=product['products'].id).update(quantity=F('quantity')-product['qty'])
                total_price += round(float(product['products'].price * product['qty']) * (1 - (product['discount']/100.0)), 2)

        self.validated_data.pop('product')
        purchase_order = PurchaseOrder(total=total_price, **self.validated_data)
        purchase_order.save()

        return purchase_order
