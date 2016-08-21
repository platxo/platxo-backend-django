from rest_framework import serializers, viewsets
from .models import Data, Information, Knowledge

# Serializers

class DataSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Data
        fields = ('id', 'name', 'created', 'updated', 'url')
        

class InformationSerializer(serializers.HyperlinkedModelSerializer):
    datas = serializers.HyperlinkedRelatedField(many=True,
                                                queryset=Data.objects.all(),
                                                view_name='data-detail')

    class Meta:
        model = Information
        fields = ('id', 'name', 'datas', 'created', 'updated', 'url')


class KnowledgeSerializer(serializers.HyperlinkedModelSerializer):
    informations = serializers.HyperlinkedRelatedField(many=True,
                                                       queryset=Information.objects.all(),
                                                       view_name='information-detail')

    class Meta:
        model = Knowledge
        fields = ('id', 'name', 'informations', 'created', 'updated', 'url')

# Viewsets

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class InformationViewSet(viewsets.ModelViewSet):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


class KnowledgeViewSet(viewsets.ModelViewSet):
    queryset = Knowledge.objects.all()
    serializer_class = KnowledgeSerializer
