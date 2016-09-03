from __future__ import unicode_literals

from django.db import models
from users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "owner"
        verbose_name_plural = "owners"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_owner(sender, instance, created, **kwargs):
        if created and instance.is_owner == True:
            owner, new = Owner.objects.get_or_create(user=instance,
                                                     first_name=instance.first_name,
                                                     last_name=instance.last_name,
                                                     email=instance.email
                                                    )


class Employed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "employed"
        verbose_name_plural = "employees"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_employed(sender, instance, created, **kwargs):
        if created and instance.is_employed == True:
            employed, new = Employed.objects.get_or_create(user=instance,
                                                           first_name=instance.first_name,
                                                           last_name=instance.last_name,
                                                           email=instance.email
                                                           )


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_customer(sender, instance, created, **kwargs):
        if created and instance.is_customer == True:
            customer, new = Customer.objects.get_or_create(user=instance,
                                                           first_name=instance.first_name,
                                                           last_name=instance.last_name,
                                                           email=instance.email
                                                           )
