from rest_framework import filters
import django_filters

from business.models import Data

class DataFilter(filters.FilterSet):

    class Meta:
        model = Data
        fields = ['business__id']
