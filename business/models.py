from __future__ import unicode_literals

from django.db import models
from djangae import fields

from accounts.models import Owner, Employed, Customer, Supplier

TAGS_CHOICES = (
('grey', 'Grey'),
('red', 'Red'),
('yellow', 'Yellow'),
('blue', 'Blue'),
('orange', 'Orange'),
('green', 'Green'),
('purple', 'Purple'),
)


class Business(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=255)
    employees = fields.RelatedSetField(Employed)
    customers = fields.RelatedSetField(Customer)
    suppliers = fields.RelatedSetField(Supplier)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'business'
        verbose_name_plural = 'business'

    def __str__(self):
        return self.name


class Data(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='datas')
    owner = models.ForeignKey(Owner, related_name='datas')
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, default='grey', choices=TAGS_CHOICES)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'data'
        verbose_name_plural = 'datas'

    def __str__(self):
        return self.name


class Information(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='informations')
    owner = models.ForeignKey(Owner, related_name='datas')
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, default='grey', choices=TAGS_CHOICES)
    datas = fields.RelatedSetField(Data)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'information'
        verbose_name_plural = 'informations'

    def __str__(self):
        return self.name


class Knowledge(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='knowledges')
    owner = models.ForeignKey(Owner, related_name='datas')
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, default='grey', choices=TAGS_CHOICES)
    informations = fields.RelatedSetField(Information)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'knowledge'
        verbose_name_plural = 'knowledges'

    def __str__(self):
        return self.name
