from __future__ import unicode_literals

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Type(models.Model):
    category = models.ForeignKey(Category, related_name='types')
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'type'
        verbose_name_plural = 'types'

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products')
    type = models.ForeignKey(Type, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    supplier = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.IntegerField()
    stock = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product/image', blank=True, null=True)
    picture = models.ImageField(upload_to='product/picture', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name