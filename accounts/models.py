from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from djangae.contrib.gauth.datastore.models import GaeAbstractDatastoreUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class PlatxoUser(GaeAbstractDatastoreUser):
    is_owner = models.BooleanField(default=False)
    is_employed = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def get_owner_profile(self):
        owner_profile = None
        if hasattr(self, 'ownerprofile'):
            owner_profile = self.ownerprofile
        return owner_profile

    def get_employed_profile(self):
        employed_profile = None
        if hasattr(self, 'employedprofile'):
            employed_profile = self.employedprofile
        return employed_profile

    def get_customer_profile(self):
        customer_profile = None
        if hasattr(self, 'customerprofile'):
            customer_profile = self.customerprofile
        return customer_profile

    class Meta:
        db_table = 'auth_user'


class Owner(models.Model):
    user = models.OneToOneField(PlatxoUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "owner"
        verbose_name_plural = "owners"

    @receiver(post_save, sender=PlatxoUser)
    def create_owner(sender, instance, created, **kwargs):
        if created:
            owner, new = Owner.objects.get_or_create(user=instance,
                                                     first_name=instance.first_name,
                                                     last_name=instance.last_name,
                                                     email=instance.email
                                                    )


class Employed(models.Model):
    user = models.OneToOneField(PlatxoUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "employed"
        verbose_name_plural = "employees"

    @receiver(post_save, sender=PlatxoUser)
    def create_employed(sender, instance, created, **kwargs):
        if created:
            employed, new = Employed.objects.get_or_create(user=instance,
                                                           first_name=instance.first_name,
                                                           last_name=instance.last_name,
                                                           email=instance.email
                                                           )


class Customer(models.Model):
    user = models.OneToOneField(PlatxoUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    @receiver(post_save, sender=PlatxoUser)
    def create_customer(sender, instance, created, **kwargs):
        if created:
            customer, new = Customer.objects.get_or_create(user=instance,
                                                           first_name=instance.first_name,
                                                           last_name=instance.last_name,
                                                           email=instance.email
                                                           )
