from rest_framework import serializers

from .models import Purchase


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Purchase
        fields = ('id', 'supplier', 'value', 'created', 'updated', 'url')
