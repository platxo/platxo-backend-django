from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from .models import Business, Tax, Data, Information, Knowledge
from accounts.models import Employee, Customer, Supplier
from . import choices


class BusinessSerializer(serializers.ModelSerializer):
    employees = serializers.PrimaryKeyRelatedField(many=True, queryset=Employee.objects.all())
    customers = serializers.PrimaryKeyRelatedField(many=True, queryset=Customer.objects.all())
    suppliers = serializers.PrimaryKeyRelatedField(many=True, queryset=Supplier.objects.all())
    picture = Base64ImageField(required=False, allow_null=True, write_only=True)
    picture_url = serializers.SerializerMethodField()

    def get_picture_url(self, obj):
        try:
            picture_url = obj.picture.url
        except Exception:
            picture_url = None
        return picture_url

    class Meta:
        model = Business
        fields = (
            'id', 'owner', 'name',
            'size', 'category', 'type',
            'currency', 'crm_points', 'country',
            'city', 'email', 'website', 'picture',
            'telephone', 'employees', 'customers',
            'suppliers', 'picture_url', 'created', 'updated', 'url')

class TaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tax
        fields = ('id', 'business', 'owner', 'name', 'rate', 'created', 'updated', 'url')


class DataSerializer(serializers.ModelSerializer):
    tag = serializers.ChoiceField(choices=choices.TAG_CHOICES, default='grey')
    informations = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    data_type = serializers.ChoiceField(choices=choices.DATA_TYPE_CHOICES, default='all')
    data_fields = serializers.ListField(required=False, child=serializers.CharField(max_length=255))
    data_filters = serializers.ListField(required=False, child=serializers.CharField(allow_blank=True, max_length=255))

    class Meta:
        model = Data
        fields = ('id', 'business', 'owner', 'name',
                  'tag', 'data_type', 'data_app', 'data_model',
                  'data_fields', 'data_filters', 'data_id',
                  'informations', 'created','updated', 'url')


class InformationSerializer(serializers.ModelSerializer):
    tag = serializers.ChoiceField(choices=choices.TAG_CHOICES, default='grey')
    datas = serializers.PrimaryKeyRelatedField(many=True, queryset=Data.objects.all())
    knowledges = serializers.PrimaryKeyRelatedField(many=True, read_only=True)


    class Meta:
        model = Information
        fields = ('id', 'business', 'owner', 'name',
                 'tag', 'datas', 'knowledges', 'created',
                 'updated', 'url')


class KnowledgeSerializer(serializers.ModelSerializer):
    tag = serializers.ChoiceField(choices=choices.TAG_CHOICES, default='grey')
    informations = serializers.PrimaryKeyRelatedField(many=True, queryset=Information.objects.all())

    class Meta:
        model = Knowledge
        fields = ('id', 'business', 'owner', 'name',
                  'tag', 'informations', 'created',
                  'updated', 'url')
