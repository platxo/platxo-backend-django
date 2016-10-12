from copy import copy

from django.db.models import F
from rest_framework import serializers

from sales.validators import OneProductOrService, UserInBusiness, DoNotUpdateAfter, CustomerPoints
from .models import Sale
from products.models import Product
from services.models import Service


class SaleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    customer_username = serializers.CharField(read_only=True)
    employee_username = serializers.CharField(read_only=True)
    products = serializers.ListField(required=False)
    services = serializers.ListField(required=False)
    # discount = serializers.IntegerField(default=0)
    subtotal = serializers.FloatField(read_only=True)
    # total_discount = serializers.FloatField(read_only=True)
    total_taxes = serializers.FloatField(read_only=True)
    customer_points = serializers.FloatField(default=0.0)
    total = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'name', 'customer',
                  'customer_username', 'employee',
                  'employee_username', 'business',
                  'payment_method', 'products',
                  'services',
                  'subtotal', 'customer_points',
                  'total_discount', 'total_taxes',
                  'total', 'created_at')
        extra_kwargs = {
            'discount': {'write_only': True}
        }
        validators = [OneProductOrService(),
                      UserInBusiness(field='employee'),
                      UserInBusiness(field='customer', anonymous=True),
                      CustomerPoints()
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
                elif prod_id.get('discount') and not (0 <= prod_id.get("discount") <= 100):
                    raise serializers.ValidationError({'product': {'id': product.id,
                                                                   'message': 'Discount not in range.'}})
                # Populate the product field
                product_object = copy(prod_id)
                product_object['details'] = {'product_category': product.product_category.id,
                                             'product_category_name': product.product_category.name,
                                             'product_type': product.product_type.id,
                                             'product_type_name': product.product_type.name,
                                             'name': product.name,
                                             'price': product.retail_price,
                                             'tax': product.tax.rate if getattr(product, 'tax') else 0
                                             }
                mapped_products.append(product_object)

            # Product now contains all information and save() van use this data.
            data['products'] = mapped_products

        if data.get('services'):
            try:
                # Extract the id of the services to search them in database. And validate initial structure.
                services_id = [service['id'] for service in data.get('services')]
            except KeyError as e:
                print (e.message)
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
                if not (0 <= serv_id.get("discount") <= 100):
                    raise serializers.ValidationError({'service': {'id': service.id,
                                                                   'message': 'Discount not in range.'}})
                # Populate the product field
                service_object = copy(serv_id)
                service_object['details'] = {'service_category': service.service_category.id,
                                             'service_category_name': service.service_category.name,
                                             'service_type': service.service_type.id,
                                             'service_type_name': service.service_type.name,
                                             'name': service.name,
                                             'price': service.price,
                                             'tax': service.tax.rate if getattr(service, 'tax') else 0
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
        tax_total = 0.0
        partial_discount = 0.0
        partial_rate = lambda price, rate: price * rate / 100.0
        get_rate = lambda rate: (1 - rate / 100.0)
        if self.validated_data.get('products'):
            for product in self.validated_data.get('products'):
                # Update product stock
                Product.objects.filter(pk=product['id']).update(quantity=F('quantity') - product['qty'])
                # Partial subtotal
                price_products = float(product['details']['price'] * product['qty'])
                subtotal += price_products
                partial_discount += partial_rate(price_products, product['discount'])
                tax_total += price_products * get_rate(product['details']['tax'])

        if self.validated_data.get('services'):
            for service in self.validated_data.get('services'):
                # Services don`t have inventory and the update is not necessary.
                # Partial subtotal
                price_services = float(service['details']['price'] * service['qty'])
                subtotal += price_services
                partial_discount += partial_rate(price_services, service['discount'])
                tax_total += price_services * get_rate(service['details']['tax'])

        total_discount = partial_discount + ((subtotal - partial_discount) * get_rate(self.validated_data['total_discount']))
        del self.validated_data['total_discount']
        total = subtotal - total_discount
        # One customer_point equals one unit in current currency.
        # This validation needs somehow to be out of this save block.
        max_points_allowed = float(get_rate(self.validated_data['business'].crm_points)) * total
        self.validated_data['customer_points'] = \
            self.validated_data['customer_points'] if \
            self.validated_data['customer_points'] <= max_points_allowed else \
            max_points_allowed

        if 'discount' in self.validated_data:
            del self.validated_data['discount']
        total += tax_total - self.validated_data['customer_points']
        sale = Sale(subtotal=round(subtotal, 2), total_discount=round(total_discount, 2),
                    total_taxes=round(tax_total, 2), total=round(total, 2), **self.validated_data)

        sale.save()

        return sale

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
