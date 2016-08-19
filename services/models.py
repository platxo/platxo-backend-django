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


class Service(models.Model):
    category = models.ForeignKey(Category, related_name='services')
    type = models.ForeignKey(Type, related_name='services')
    name = models.CharField(max_length=255)
    description = models.TextField()
    supplier = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image = models.ImageField(upload_to='service/image', blank=True, null=True)
    picture = models.ImageField(upload_to='service/picture', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'service'
        verbose_name_plural = 'services'

    def __str__(self):
        return self.name