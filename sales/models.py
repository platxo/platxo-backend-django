from __future__ import unicode_literals

from django.db import models
from products.models import Product

class Sale(models.Model):
    customer = models.CharField(max_length=255)
    product = models.ForeignKey(Product, related_name='products')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'sale'
        verbose_name_plural = 'sales'

    def __str__(self):
        return self.customer