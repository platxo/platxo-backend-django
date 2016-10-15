from __future__ import unicode_literals

from decimal import *

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Customer
from business.models import Business
from sales.models import Sale


class Point(models.Model):
    customer = models.ForeignKey(Customer, related_name='points')
    business = models.ForeignKey(Business, related_name='points')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'point'
        verbose_name_plural = 'points'
        unique_together = ("customer", "business")

    def __str__(self):
        return self.customer.user.username

    @receiver(post_save, sender=Sale)
    def create_user_points(sender, instance, created, **kwargs):
        """
        Add customer points to the customer. After a purchase is made.

        Validate the business allows collection of user points and add the corresponding
        points to customer.

        :param instante:
        :param created:
        :param kwargs:
        :return:
        """
        if created and instance.customer and not instance.sale_replacement:
            # Only customers deserve points
            # And the sale must no replace other sale.
            try:
                point = Point.objects.get(customer=instance.customer, business=instance.business)
            except Point.DoesNotExist:
                point = Point(customer=instance.customer, business=instance.business, balance=0)

            # Validate how many points the business allows from the purchase.
            points_percentage = getattr(instance.business, 'crm_points', 0) if getattr(instance.business, 'crm_points') else 0
            gained_points = (points_percentage/100.0) * instance.total
            point.balance += Decimal(gained_points-instance.customer_points)

            point.save()
