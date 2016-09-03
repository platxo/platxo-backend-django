from __future__ import unicode_literals

from django.db import models
from djangae import fields

from django.contrib.auth.models import User
from djangae.contrib.gauth.datastore.models import GaeDatastoreUser
from accounts.models import Owner, Employed, Customer

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
    name = models.CharField(max_length=255)
    #owner = models.ForeignKey(Owner, related_name='business')
    #employees = fields.RelatedSetField(Employed)
    #customers = fields.RelatedSetField(Customer)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'business'
        verbose_name_plural = 'business'

    def __str__(self):
        return self.name


class Data(models.Model):
    #business = models.ForeignKey(Business, related_name='products')
    user = models.ForeignKey(GaeDatastoreUser, related_name='datas')
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
    user = models.ForeignKey(GaeDatastoreUser, related_name='informations')
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
    user = models.ForeignKey(GaeDatastoreUser, related_name='knowledges')
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
