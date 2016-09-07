from rest_framework import serializers

from .models import Business, Data, Information, Knowledge, TAGS_CHOICES
from accounts.models import Owner, Employed, Customer, Supplier


class BusinessSerializer(serializers.HyperlinkedModelSerializer):
    employees = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Employed.objects.all(),
        view_name='employed-detail'
    )
    customers = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Customer.objects.all(),
        view_name='customer-detail'
    )
    suppliers = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Supplier.objects.all(),
        view_name='supplier-detail'
    )

    class Meta:
        model = Business
        fields = ('id', 'owner', 'name', 'employees', 'customers', 'suppliers', 'created', 'updated', 'url')


class DataSerializer(serializers.HyperlinkedModelSerializer):
    tag = serializers.ChoiceField(choices=TAGS_CHOICES, default='grey')

    class Meta:
        model = Data
        fields = ('id', 'business', 'owner', 'name', 'tag', 'created', 'updated', 'url')


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    tag = serializers.ChoiceField(choices=TAGS_CHOICES, default='grey')
    datas = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Data.objects.all(),
        view_name='data-detail'
    )


    class Meta:
        model = Information
        fields = ('id', 'business', 'owner', 'name', 'tag', 'datas', 'created', 'updated', 'url')


class KnowledgeSerializer(serializers.HyperlinkedModelSerializer):
    tag = serializers.ChoiceField(choices=TAGS_CHOICES, default='grey')
    informations = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Information.objects.all(),
        view_name='information-detail'
    )

    class Meta:
        model = Knowledge
        fields = ('id', 'business', 'owner', 'name', 'tag', 'informations', 'created', 'updated', 'url')
