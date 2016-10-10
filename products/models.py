from __future__ import unicode_literals

from django.db import models
from djangae import fields, storage

from business.models import Business
from accounts.models import Employee, Supplier
from business.models import Tax

public_storage = storage.CloudStorage(google_acl='public-read')

class Location(models.Model):
    business = models.ForeignKey(Business, related_name='locations')
    employee = models.ForeignKey(Employee, related_name='locations')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def __str__(self):
        return self.name

class Section(models.Model):
    business = models.ForeignKey(Business, related_name='sections')
    employee = models.ForeignKey(Employee, related_name='sections')
    location = models.ForeignKey(Location, related_name='sections')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'section'
        verbose_name_plural = 'sections'

    def __str__(self):
        return self.name

class ProductCategory(models.Model):
    business = models.ForeignKey(Business, related_name='product_categories')
    employee = models.ForeignKey(Employee, related_name='product_categories')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'product_category'
        verbose_name_plural = 'product_categories'

    def __str__(self):
        return self.name


class ProductType(models.Model):
    business = models.ForeignKey(Business, related_name='product_types')
    employee = models.ForeignKey(Employee, related_name='product_types')
    product_category = models.ForeignKey(ProductCategory, related_name='product_types')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'product_type'
        verbose_name_plural = 'product_types'

    def __str__(self):
        return self.name


class Product(models.Model):
    business = models.ForeignKey(Business, related_name='products')
    employee = models.ForeignKey(Employee, related_name='products')
    tax = models.ForeignKey(Tax, related_name='products', blank=True, null=True)
    supplier = models.ForeignKey(Supplier, related_name='products', blank=True, null=True)
    product_category = models.ForeignKey(ProductCategory, related_name='products')
    product_type = models.ForeignKey(ProductType, related_name='products')
    location = models.ForeignKey(Location, related_name='products', blank=True, null=True)
    section = models.ForeignKey(Section, related_name='products', blank=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    supply_price = models.DecimalField(max_digits=10, decimal_places=2)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.BooleanField(default=True)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product/image', storage=public_storage, blank=True, null=True)
    picture = models.ImageField(upload_to='product/picture', storage=public_storage, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Analytics module registration.
    analytics_fields = ('id', 'name', 'inventory', 'quantity', 'retail_price', 'product_category')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
