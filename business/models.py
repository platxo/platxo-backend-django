# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djangae import fields
from .choices import *
from accounts.models import Owner, Employee, Customer, Supplier

class Business(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='business')
    name = models.CharField(max_length=255)
    country = models.CharField(choices=COUNTRY_CHOICES)
    city = models.CharField(max_length=255)
    currency = models.CharField(choices=CURRENCY_CHOICES)
    crm_points = models.IntegerField(max_length=2, choices=CRM_POINTS_CHOICES, default=ZERO)
    category = models.CharField(choices=CATEGORY_CHOICES)
    type = models.CharField(choices=TYPE_CHOICES)
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


class Data(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='datas')
    owner = models.ForeignKey(Owner, related_name='datas')
    name = models.CharField(max_length=255)
    tag = models.CharField(max_length=255, default='grey', choices=TAGS_CHOICES)
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
    tag = models.CharField(max_length=255, default='grey', choices=TAGS_CHOICES)
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
    tag = models.CharField(max_length=255, default='grey', choices=TAGS_CHOICES)
    informations = fields.RelatedSetField(Information, related_name='knowledges')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'knowledge'
        verbose_name_plural = 'knowledges'

    def __str__(self):
        return self.name
