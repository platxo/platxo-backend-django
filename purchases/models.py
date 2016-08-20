from __future__ import unicode_literals

from django.db import models

class Purchase(models.Model):
    supplier = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'purchase'
        verbose_name_plural = 'purchases'

    def __str__(self):
        return self.supplier