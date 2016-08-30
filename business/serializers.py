from rest_framework import serializers

from .models import Data, Information, Knowledge


class DataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Data
        fields = ('id', 'user', 'name', 'created', 'updated', 'url')


class InformationSerializer(serializers.HyperlinkedModelSerializer):
    datas = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Data.objects.all(),
        view_name='data-detail'
    )

    class Meta:
        model = Information
        fields = ('id', 'user', 'name', 'datas', 'created', 'updated', 'url')


class KnowledgeSerializer(serializers.HyperlinkedModelSerializer):
    informations = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Information.objects.all(),
        view_name='information-detail'
    )

    class Meta:
        model = Knowledge
        fields = ('id', 'user', 'name', 'informations', 'created', 'updated', 'url')
