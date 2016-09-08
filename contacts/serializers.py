from rest_framework import serializers

from .models import Contact


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'claim', 'customer', 'state', 'created', 'updated', 'url')
