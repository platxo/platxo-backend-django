from __future__ import unicode_literals

from django.db import models
from djangae import fields
from business.models import Business
from accounts.models import Employee, Customer
from products.models import Product
from services.models import Service


class Sale(models.Model):
    CASH = 'cash'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    PAYMENT_CHOICES = (
        (CASH, 'cash'),
        (CREDIT_CARD, 'credit card'),
        (DEBIT_CARD, 'debit card')
    )

    business = models.ForeignKey(Business, related_name='sales')
    employee = models.ForeignKey(Employee, related_name='sales')
    customer = models.ForeignKey(Customer, related_name='sales', blank=True, null=True)
    products = fields.RelatedSetField(Product, related_name='sales')
    services = fields.RelatedSetField(Service, related_name='sales')
    payment = models.CharField(max_length=150, choices=PAYMENT_CHOICES)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return self.customer
        

class PurchaseOrder(models.Model):
    CASH = 'cash'
    CREDIT_CARD = 'credit_card'
    DEBIT_CARD = 'debit_card'
    PAYMENT_CHOICES = (
        (CASH, 'cash'),
        (CREDIT_CARD, 'credit card'),
        (DEBIT_CARD, 'debit card')
    )

    # Information of the actors involved in the transaction.
    employee = models.ForeignKey(Employee)
    employee_username = models.CharField(max_length=255, blank=True, null=True)

    business = models.ForeignKey(Business)
    business_name = models.CharField(max_length=255, blank=True, null=True)

    customer = models.ForeignKey(Customer, blank=True, null=True)
    customer_username = models.CharField(max_length=255, blank=True, null=True)

    # Payment method used in the transaction. The customer points are optional.
    payment_method = models.CharField(max_length=150, choices=PAYMENT_CHOICES)

    # Products and services bought
    # An array field expecting the contents {
    #                                      id: product/service id,
    #                                      qty: total items bought,
    #                                      discount: (optional} Integer number of the independent discount to the item.}
    products = fields.JSONField()
    services = fields.JSONField()

    # The value before applying any deduction or increment due to taxex, points
    subtotal = models.FloatField(help_text='Brute total')
    # Percentage of discount applied to subtotal
    discount = models.IntegerField(help_text='A discount to apply to the whole purchase', blank=True, default=0)
    # Net value received
    total = models.FloatField(help_text='The final and payed value')

    # In case the order has been canceled, instead of deleting the record, it is canceled.
    OK = 'ACCEPTED'
    CANCEL = 'CANCELED'
    status_choices = ((OK, OK), (CANCEL, CANCEL))
    status = models.CharField(max_length=10, choices=status_choices, default=OK)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Products: {product}, by: {employee} in: {business}".format(product=len(self.products), employee=self.employee.__str__(), business=self.business.name)

    class Meta():
        ordering = ('-created_at',)
