from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from business import choices as busines_choices

PARAMETRIZATIONS_SOURCES = {
    'tag_choices' : busines_choices.TAG_CHOICES,
    'size_choices' : busines_choices.SIZE_CHOICES,
    'country_choices' : busines_choices.COUNTRY_CHOICES,
    'currency_choices' : busines_choices.CURRENCY_CHOICES,
    'crm_points_choices' : busines_choices.CRM_POINTS_CHOICES,
    'category_choices' : busines_choices.CATEGORY_CHOICES,
    'type_choices' : busines_choices.TYPE_CHOICES,
    'type_query_choices' : busines_choices.TYPE_QUERY_CHOICES,
}

class ParametrizationViewSet(viewsets.ViewSet):

    def list(self, request):
        keys = PARAMETRIZATIONS_SOURCES.keys()
        return Response(keys)

    # def retrieve(self, request, pk=None):
    #     try:
    #         return Response(PARAMETRIZATIONS_SOURCES[pk])
    #     except KeyError:
    #         return Response({'Error': 'Parametrization not found.'}, status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, pk=None):
        try:
            return Response(dict(PARAMETRIZATIONS_SOURCES[pk]))
        except KeyError:
            return Response({'Error': 'Parametrization not found.'}, status.HTTP_404_NOT_FOUND)

    # def retrieve(self, request, pk=None):
    #     try:
    #         d = dict(PARAMETRIZATIONS_SOURCES[pk])
    #         return Response(dict((v,k) for k,v in d.iteritems()))
    #     except KeyError:
    #         return Response({'Error': 'Parametrization not found.'}, status.HTTP_404_NOT_FOUND)
