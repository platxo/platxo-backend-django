from __future__ import unicode_literals

from django.db import models
from business.models import Business
from business.models import Customer
from products.models import Product
from services.models import Service

class Contact(models.Model):
    business = models.ForeignKey(Business, related_name='contacts')
    customer = models.ForeignKey(Customer, related_name='contacts')
    claim = models.CharField(max_length=255)
    state = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return self.claim

class Promotion(models.Model):
    business = models.ForeignKey(Business, related_name='promotions')
    product = models.ForeignKey(Product, blank=True, null=True, related_name='promotions')
    service = models.ForeignKey(Service, blank=True, null=True, related_name='promotions')
    description = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'promotion'
        verbose_name_plural = 'promotions'

    def __str__(self):
        return self.business
