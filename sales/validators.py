from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers

from business.models import Business
from customers.models import Point


class OneProductOrService(object):
    """
    Ensure at least one product or service comes.
    """
    def __init__(self):
        pass

    def __call__(self, attrs):
        if not attrs.get('products') and not attrs.get('services'):
            raise serializers.ValidationError("Include at least one product or service.")


class UserInBusiness(object):
    """
    Validate  that employee and customer belongs to the business.
    """
    def __init__(self, field, anonymous=False):
        self.field = field
        self.anonymous = anonymous

    def __call__(self, attrs):
        if self.anonymous and not attrs.get(self.field):
            return
        try:
            query_args = {'pk': attrs['business'].id, self.field + 's__contains': attrs[self.field]}
            if not Business.objects.filter(**query_args).exists():
                raise serializers.ValidationError({self.field: "{field} does not belong to Business".format(field=self.field)})

        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Exception as e:
            print e
            raise serializers.ValidationError(e.message)

        attrs[self.field + '_username'] = attrs[self.field].user.username


class DoNotUpdateAfter(object):
    """
    Validate that the object is not being updated after a given time in minutes and more than once neither.
    For possible PUT feature
    """
    def __init__(self, time=0):
        self.time = time

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)

    def __call__(self, attrs):
        now = timezone.now()
        if hasattr(self, 'instance') and hasattr(self.instance, 'created_at') and self.instance.created_at < (now+timedelta(minutes=-self.time)):
            raise serializers.ValidationError({'created_at': 'Operation after allowed time.'})


class CustomerPoints(object):
    """
    Validate the user can use his/her customer points ensuring he owns the points used and that those points belongs
    to the business where the purchase is being made.
    """
    def __init__(self):
        pass

    def __call__(self, attrs):
        if not attrs['customer_points']:
            # No validation is necessary
            return
        elif attrs['customer_points'] and not attrs.get('customer'):
            raise serializers.ValidationError({'customer_points': 'Sent without customer.'})

        # Validate the user has points in the business
        try:
            points_in_business = Point.objects.get(business=attrs['business'], customer=attrs['customer'])
        except Point.DoesNotExist:
            raise serializers.ValidationError({'customer_points'})

        if points_in_business.balance and points_in_business.balance < attrs['customer_points']:
            raise serializers.ValidationError({'customer_points': 'Not enough points.'})

