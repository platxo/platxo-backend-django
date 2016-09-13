from __future__ import unicode_literals

from django.db import models
from accounts.models import Supplier

class Purchase(models.Model):
    supplier = models.ForeignKey(Supplier, related_name='purchases')
    value = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'

    def __str__(self):
        return self.supplier
