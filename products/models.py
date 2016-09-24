from __future__ import unicode_literals

from django.db import models
from djmoney.models.fields import MoneyField

from business.models import Business
from accounts.models import Employee


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
    product_category = models.ForeignKey(ProductCategory, related_name='products')
    product_type = models.ForeignKey(ProductType, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    supplier = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.BooleanField(default=False)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='product/image', blank=True, null=True)
    picture = models.ImageField(upload_to='product/picture', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name
