from __future__ import unicode_literals

from django.db import models
from djangae import fields, storage

from business.models import Business, Tax
from accounts.models import Employee

public_storage = storage.CloudStorage(google_acl='public-read')


class ServiceCategory(models.Model):
    business = models.ForeignKey(Business, related_name='products')
    employee = models.ForeignKey(Employee, related_name='services')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'service_category'
        verbose_name_plural = 'service_categories'

    def __str__(self):
        return self.name


class ServiceType(models.Model):
    business = models.ForeignKey(Business, related_name='products')
    employee = models.ForeignKey(Employee, related_name='services')
    service_category = models.ForeignKey(ServiceCategory, related_name='service_types')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'service_type'
        verbose_name_plural = 'service_types'

    def __str__(self):
        return self.name


class Service(models.Model):
    business = models.ForeignKey(Business, related_name='services')
    employee = models.ForeignKey(Employee, related_name='services')
    tax = models.ForeignKey(Tax, related_name='services', blank=True, null=True)
    service_category = models.ForeignKey(ServiceCategory, related_name='services')
    service_type = models.ForeignKey(ServiceType, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='service/image', storage=public_storage, blank=True, null=True)
    picture = models.ImageField(upload_to='service/picture', storage=public_storage, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return self.name
