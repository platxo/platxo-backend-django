from __future__ import unicode_literals

from django.db import models
from djangae import fields
from products.models import Product
from services.models import Service


class Sale(models.Model):
    customer = models.CharField(max_length=255)
    products = fields.RelatedSetField(Product)
    services = fields.RelatedSetField(Service)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return self.customer
