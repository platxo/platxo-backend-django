from __future__ import unicode_literals

from django.db import models
from accounts.models import Customer
from business.models import Business

class Point(models.Model):
    customer = models.ForeignKey(Customer, related_name='points')
    business = models.ForeignKey(Business, related_name='points')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'point'
        verbose_name_plural = 'points'

    def __str__(self):
        return self.customer.user.username
