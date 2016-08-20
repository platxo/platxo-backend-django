from rest_framework import serializers, viewsets
from .models import Contact

# Serializers


class ContactSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Contact
        fields = ('id', 'claim', 'customer', 'state', 'created', 'updated', 'url')

# Viewsets

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer