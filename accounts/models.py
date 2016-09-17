from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from djangae.contrib.gauth.datastore.models import Group


class Owner(models.Model):
    """
    Owner representation of the user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        verbose_name = "owner"
        verbose_name_plural = "owners"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_owner(sender, instance, created, **kwargs):
        """
        After create
        :param instance:
        :param created:
        :param kwargs:
        :return:
        """
        if created and instance.is_owner is True:
            owner, new = Owner.objects.get_or_create(user=instance)
            group = Group.objects.get(name='owner')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_owner(sender, instance, **kwargs):
        """
        After update
        :param instance:
        :param kwargs:
        :return:
        """
        if instance.is_owner and not hasattr(instance, 'owner'):
            owner, new = Owner.objects.get_or_create(user=instance)
            group = Group.objects.get(name='owner')
            instance.groups.add(group)
            instance.save()
        elif instance.is_owner:
            instance.owner.save()


class Employee(models.Model):
    """
    Employee representation of the user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_employee(sender, instance, created, **kwargs):
        """
        After create
        :param instance:
        :param created:
        :param kwargs:
        :return:
        """
        if created and instance.is_employee is True:
            employee, new = Employee.objects.get_or_create(user=instance)
            group = Group.objects.get(name='employee')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_employee(sender, instance, **kwargs):
        """
        After update
        :param instance:
        :param kwargs:
        :return:
        """
        if instance.is_employee and not hasattr(instance, 'employee'):
            employee, new = Employee.objects.get_or_create(user=instance)
            group = Group.objects.get(name='employee')
            instance.groups.add(group)
            instance.save()
        elif instance.is_employee:
            instance.employee.save()


class Customer(models.Model):
    """
    Customer representation of the user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_customer(sender, instance, created, **kwargs):
        """
        After create
        :param instance:
        :param created:
        :param kwargs:
        :return:
        """
        if created and instance.is_customer is True:
            customer, new = Customer.objects.get_or_create(user=instance)
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_customer(sender, instance, **kwargs):
        """
        After update
        :param instance:
        :param kwargs:
        :return:
        """
        if instance.is_customer and not hasattr(instance, 'customer'):
            customer, new = Customer.objects.get_or_create(user=instance)
            group = Group.objects.get(name='customer')
            instance.groups.add(group)
            instance.save()
        elif instance.is_customer:
            instance.customer.save()


class Supplier(models.Model):
    """
    Supplier representation of the user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class meta:
        verbose_name = "supplier"
        verbose_name_plural = "suppliers"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_supplier(sender, instance, created, **kwargs):
        """
        After create
        :param instance:
        :param created:
        :param kwargs:
        :return:
        """
        if created and instance.is_supplier is True:
            supplier, new = Supplier.objects.get_or_create(user=instance)
            group = Group.objects.get(name='supplier')
            instance.groups.add(group)
            instance.save()

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def save_supplier(sender, instance, **kwargs):
        """
        After update
        :param instance:
        :param kwargs:
        :return:
        """
        if instance.is_supplier and not hasattr(instance, 'supplier'):
            supplier, new = Supplier.objects.get_or_create(user=instance)
            group = Group.objects.get(name='supplier')
            instance.groups.add(group)
            instance.save()

        elif instance.is_supplier:
            instance.supplier.save()
