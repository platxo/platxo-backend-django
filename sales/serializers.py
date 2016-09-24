from copy import copy

from django.db.models import F
from rest_framework import serializers

from sales.validators import OneProductOrService, UserInBusiness, DoNotUpdateAfter
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
    customer_username = serializers.CharField(read_only=True)
    employee_username = serializers.CharField(read_only=True)
    products = serializers.ListField(required=False)
    services = serializers.ListField(required=False)
    subtotal = serializers.FloatField(read_only=True)
    discount = serializers.IntegerField(default=0)
    total = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = ('id', 'customer',
                  'customer_username', 'employee',
                  'employee_username', 'business',
                  'payment_method', 'products',
                  'services', 'discount',
                  'subtotal', 'total', 'created_at')
        validators = [OneProductOrService(),
                      UserInBusiness(field='employee'),
                      UserInBusiness(field='customer', anonymous=True),
                      # DoNotUpdateAfter(time=5)
                      ]

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
            # Validate each product field.
            # current_products = self.instance.products if hasattr(self.instance, 'products') else list() # PUT Feature
            for prod_id in data.get('products'):
                # Get the product with its id
                product = next(prod for prod in products if prod.id == prod_id['id'])
                if not prod_id.get('qty'):
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Missing or invalid qty.'}})
                # There should be enough products in stock
                # Code for future PUT feature
                # try:
                #     current_product = next(prod for prod in current_products if prod.id == prod_id['id'])
                # except StopIteration as e:
                #     # The products wasn't registered in the original purchase
                #     current_product = 0
                # expected_stock = current_product
                elif prod_id.get('qty') > product.quantity:
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Not enough products on stock.'}})
                # Discount must be between 0% and 100% and is optional
                if not prod_id.get("discount"):
                    prod_id['discount'] = 0
                elif prod_id.get('discount') and not(0 <= prod_id.get("discount") <= 100):
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Discount not in range.'}})
                # Populate the product field
                product_object = copy(prod_id)
                product_object['details'] = {'product_category': product.product_category.id,
                                              'product_category_name': product.product_category.name,
                                              'product_type': product.product_type.id,
                                              'product_type_name': product.product_type.name,
                                              'name': product.name,
                                              'price': product.price
                                              }
                mapped_products.append(product_object)

            # Product now contains all information and save() van use this data.
            data['products'] = mapped_products

        if data.get('services'):
            try:
                # Extract the id of the services to search them in database. And validate initial structure.
                services_id = [service['id'] for service in data.get('services')]
            except KeyError as e:
                print e.message
                raise serializers.ValidationError({'service': 'Missing id.'})

            # All services exists and belongs to the same business
            services = list(Service.objects.filter(pk__in=services_id, business=data.get('business').id))

            # If both don't match it's an error
            if len(services_id) != len(services):
                raise serializers.ValidationError({'service': 'Duplicated or missing id.'})

            mapped_services = list()
            # Validate each product field.
            for serv_id in data.get('services'):
                # Get the service with its id
                service = next(serv for serv in services if serv.id == serv_id['id'])
                if not serv_id.get('qty'):
                    raise serializers.ValidationError({'service': {'id': service.id,
                                                                   'message': 'Missing or invalid qty.'}})
                # Discount must be between 0% and 100%
                if not serv_id.get("discount"):
                    serv_id['discount'] = 0
                if not(0 <= serv_id.get("discount") <= 100):
                    raise serializers.ValidationError({'service': {'id': service.id,
                                                                   'message': 'Discount not in range.'}})
                # Populate the product field
                service_object = copy(serv_id)
                service_object['details'] = {'service_category': service.service_category.id,
                                             'service_category_name': service.service_category.name,
                                             'service_type': service.service_type.id,
                                             'service_type_name': service.service_type.name,
                                             'name': service.name,
                                             'price': service.price
                                             }
                mapped_services.append(service_object)

            # Product now contains all information and save() van use this data.
            data['services'] = mapped_services

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
        subtotal = 0.0
        if self.validated_data.get('products'):
            for product in self.validated_data.get('products'):
                Product.objects.filter(pk=product['id']).update(quantity=F('quantity')-product['qty'])
                subtotal += float(product['details']['price'] * product['qty']) * (1 - (product['discount']/100.0))

        if self.validated_data.get('services'):
            for service in self.validated_data.get('services'):
                subtotal += float(service['details']['price'] * service['qty']) * (1 - (service['discount'] / 100.0))

        total = round(subtotal * (1 - (self.validated_data['discount'] / 100.0)), 2)
        purchase_order = PurchaseOrder(subtotal=subtotal, total=round(total, 2), **self.validated_data)
        purchase_order.save()

        return purchase_order

    def update(self, instance, validated_data):
        """
        Performs an update in the original order stored. Re-calculating the stock of products.

        For traceability it keeps the old items.

        :param instance:
        :param validated_data:
        :return:
        """
        # Products assignment
        pass
