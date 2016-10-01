from rest_framework import serializers

from .models import Contact, Promotion


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'claim', 'customer', 'state', 'created', 'updated', 'url')

class PromotionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Promotion
        fields = ('id',
                  'business',
                  'employee',
                  'product',
                  'service',
                  'title',
                  'description',
                  'created',
                  'updated',
                  'url')
