from __future__ import unicode_literals

from django.db import models
from djangae import fields
from business.models import Business
from accounts.models import Employee, Customer
from products.models import Product
from services.models import Service


class Sale(models.Model):
    business = models.ForeignKey(Business, related_name='sales')
    employed = models.ForeignKey(Employee, related_name='sales')
    customer = models.ForeignKey(Customer, related_name='sales')
    products = fields.RelatedSetField(Product)
    services = fields.RelatedSetField(Service)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

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

    employee = models.ForeignKey(Employee)
    employee_username = models.CharField(max_length=255, blank=True, null=True)
    business = models.ForeignKey(Business)
    business_name = models.CharField(max_length=255, blank=True, null=True)
    customer = models.ForeignKey(Customer, blank=True, null=True)
    customer_username = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=150, choices=PAYMENT_CHOICES)
    products = fields.JSONField()
    services = fields.JSONField()
    total = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Products: {product}, by: {employee} in: {business}".format(product=len(self.products), employee=self.employee.__str__(), business=self.business.name)

    class Meta():
        ordering = ('-created_at',)
