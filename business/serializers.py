from rest_framework import serializers

from .models import Business, Data, Information, Knowledge, TAGS_CHOICES
from accounts.models import Employee, Customer, Supplier


class BusinessSerializer(serializers.ModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(many=True, queryset=Employee.objects.all())
    customers = serializers.PrimaryKeyRelatedField(many=True, queryset=Customer.objects.all())
    suppliers = serializers.PrimaryKeyRelatedField(many=True, queryset=Supplier.objects.all())


    class Meta:
        model = Business
        fields = ('id', 'owner', 'name', 'employees', 'customers', 'suppliers', 'created', 'updated', 'url')


class DataSerializer(serializers.ModelSerializer):
    tag = serializers.ChoiceField(choices=TAGS_CHOICES, default='grey')

    class Meta:
        model = Data
        fields = ('id', 'business', 'owner', 'name', 'tag', 'created', 'updated', 'url')


class InformationSerializer(serializers.ModelSerializer):
    tag = serializers.ChoiceField(choices=TAGS_CHOICES, default='grey')
    datas = serializers.PrimaryKeyRelatedField(many=True, queryset=Data.objects.all())


    class Meta:
        model = Information
        fields = ('id', 'business', 'owner', 'name', 'tag', 'datas', 'created', 'updated', 'url')


class KnowledgeSerializer(serializers.ModelSerializer):
    tag = serializers.ChoiceField(choices=TAGS_CHOICES, default='grey')
    informations = serializers.PrimaryKeyRelatedField(many=True, queryset=Information.objects.all())

    class Meta:
        model = Knowledge
        fields = ('id', 'business', 'owner', 'name', 'tag', 'informations', 'created', 'updated', 'url')
