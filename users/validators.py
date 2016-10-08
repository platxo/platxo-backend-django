from datetime import timedelta
from django.utils import timezone
from rest_framework import serializers

from users.models import ForgotPassword


class NotBeforeValidator(object):
    """
    Validates the code has not expired
    """
    def __init__(self, field, time):
        self.model = ForgotPassword
        self.time_limit = time
        self.field = field

    def __call__(self, attrs):
        try:
            recovery = self.model.objects.get(user_email=attrs.get('email'), code=attrs.get('code'))
        except self.model.DoesNotExist:
            raise serializers.ValidationError({'code': 'Not found.'})

        if recovery.status is recovery.INVALID or getattr(recovery, self.field) > timezone.now()-timedelta(minutes=self.time_limit):
            raise serializers.ValidationError({'code': 'Expired.'})


class NotBeforeUpdateValidator(object):
    """
    Validates the code has not expired
    """
    def __init__(self, field, time):
        self.model = ForgotPassword
        self.time_limit = time
        self.field = field

    def __call__(self, attrs):
        try:
            recovery = self.model.objects.get(token=attrs.get('token'))
        except self.model.DoesNotExist:
            raise serializers.ValidationError({'code': 'Not found.'})

        if recovery.status is recovery.INVALID or getattr(recovery, self.field) > timezone.now()-timedelta(minutes=self.time_limit):
            raise serializers.ValidationError({'code': 'Expired.'})


class BothMatch(object):
    """
    Validates the code has not expired
    """
    def __init__(self, reference, compare):
        self.reference = reference
        self.compare = compare

    def __call__(self, attrs):
        if attrs.get(self.reference) != attrs.get(self.compare):
            raise serializers.ValidationError({'password': 'Password do not match.'})
