from __future__ import unicode_literals

from django.db import models

class Contact(models.Model):
    claim = models.CharField(max_length=255)
    customer = models.CharField(max_length=255)
    state = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'contact'
        verbose_name_plural = 'contacts'

    def __str__(self):
        return self.claim