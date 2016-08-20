from rest_framework import serializers, viewsets
from .models import Purchase

# Serializers


class PurchaseSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Purchase
        fields = ('id', 'supplier', 'value', 'created', 'updated', 'url')

# Viewsets

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer