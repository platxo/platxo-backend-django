from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from djangae.contrib.gauth.datastore.models import Group


class Owner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "owner"
        verbose_name_plural = "owners"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_owner(sender, instance, created, **kwargs):
        if created and instance.is_owner is True:
            owner, new = Owner.objects.get_or_create(user=instance)
            group = Group.objects.get(name='owner')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_owner(sender, instance, **kwargs):
        if instance.is_owner is True:
            instance.owner.save()


class Employed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "employed"
        verbose_name_plural = "employees"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_employed(sender, instance, created, **kwargs):
        if created and instance.is_employed is True:
            employed, new = Employed.objects.get_or_create(user=instance)
            group = Group.objects.get(name='employed')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_employed(sender, instance, **kwargs):
        if instance.is_employed is True:
            instance.employed.save()


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_customer(sender, instance, created, **kwargs):
        if created and instance.is_customer is True:
            customer, new = Customer.objects.get_or_create(user=instance)
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_customer(sender, instance, **kwargs):
        if instance.is_customer is True:
            instance.customer.save()

class Supplier(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_customer(sender, instance, created, **kwargs):
        if created and instance.is_supplier is True:
            supplier, new = Supplier.objects.get_or_create(user=instance)
            group = Group.objects.get(name='supplier')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_supplier(sender, instance, **kwargs):
        if instance.is_supplier is True:
            instance.supplier.save()
