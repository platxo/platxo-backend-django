# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djangae import fields
from . import choices
from accounts.models import Owner, Employee, Customer, Supplier


class Business(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=255)
    size = models.CharField(choices=choices.SIZE_CHOICES)
    category = models.CharField(choices=choices.CATEGORY_CHOICES)
    type = models.CharField(choices=choices.TYPE_CHOICES)
    currency = models.CharField(choices=choices.CURRENCY_CHOICES)
    crm_points = models.IntegerField(max_length=2, choices=choices.CRM_POINTS_CHOICES, default=choices.ZERO)
    country = models.CharField(choices=choices.COUNTRY_CHOICES)
    city = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    website = models.URLField(max_length=200, blank=True)
    telephone = models.CharField(max_length=20)
    employees = fields.RelatedSetField(Employee, related_name='business')
    customers = fields.RelatedSetField(Customer, related_name='business')
    suppliers = fields.RelatedSetField(Supplier, related_name='business')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'business'
        verbose_name_plural = 'business'

    def __str__(self):
        return self.name

class Tax(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='taxes')
    owner = models.ForeignKey(Owner, related_name='taxes')
    name = models.CharField(max_length=255)
    rate = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'tax'
        verbose_name_plural = 'taxes'

    def __str__(self):
        return self.name



class Data(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='datas')
    owner = models.ForeignKey(Owner, related_name='datas')
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, default='grey', choices=choices.TAG_CHOICES)
    data_app = models.CharField(max_length=255, blank=True, null=True)
    data_model = models.CharField(max_length=255, blank=True, null=True)
    data_fields = fields.ListField(models.CharField(max_length=255))
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    tag = models.CharField(max_length=255, default='grey', choices=choices.TAG_CHOICES)
    datas = fields.RelatedSetField(Data, related_name='informations')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

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
    tag = models.CharField(max_length=255, default='grey', choices=choices.TAG_CHOICES)
    informations = fields.RelatedSetField(Information, related_name='knowledges')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'knowledge'
        verbose_name_plural = 'knowledges'

    def __str__(self):
        return self.name
