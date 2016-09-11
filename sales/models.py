from __future__ import unicode_literals

from django.db import models
from djangae import fields
from business.models import Business
from accounts.models import Employee, Customer
from products.models import Product
from services.models import Service


class Order(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return self.id

class Sale(models.Model):
    business = models.ForeignKey(Business, related_name='sales')
    employee = models.ForeignKey(Employee, related_name='sales')
    customer = models.ForeignKey(Customer, related_name='sales')
    products = fields.RelatedSetField(Product, related_name='sales')
    services = fields.RelatedSetField(Service, related_name='sales')
    total = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return self.customer

class Receipt(models.Model):
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'receipt'
        verbose_name_plural = 'receipts'

    def __str__(self):
        return self.id
