import operator
from django.apps import apps
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from business import choices


class AnalyticsTest(viewsets.ViewSet):

    def get_queryset(self):
        """
        Get the specified fields from the specified model.
        :return:
        """
        query_type = self.request.query_params.get('type')
        app = self.request.query_params.get('app')
        model = self.request.query_params.get('model')
        fields = self.request.query_params.getlist('fields', [])
        filters = self.request.query_params.getlist('filters', [])
        query_id = self.request.query_params.get('id')

        # Business queryset filter
        business = self.request.user.owner.business.all()

        if app and model:
            a = apps.get_app_config(app).get_model(model)
        else:
            return None

        if query_type == choices.ALL:
            return a.objects.filter(business__in=business).values(*fields)
        elif query_type == choices.SINGLE:
            return [a.objects.filter(business__in=business).values(*fields).get(pk=query_id)]
        elif query_type == choices.FILTER:
            queries = []
            for (query_field, query_filter) in zip(fields, filters):
                kwargs = {query_field: query_filter}
                if query_filter is not u'':
                    queries.append(Q(**kwargs))
            q = reduce(operator.or_, queries)
            return list(a.objects.filter(business__in=business).filter(q).values(*fields))
        else:
            return None

    def list(self, request):
        """
        Return the available operations or the requested information.

        Note: An application to be eligible in the analytics module must have its apps.AppConfig.analytics=True
        And a model must have `analytics_fields` as a variable and a tuple with the desired fields ex. (name, pk)

        :param request:
        :return:
        """
        # Only owners can access and only their own information
        if not self.request.user.is_owner and not self.request.user.is_owner:
            return Response({'error': 'You are not owner.'}, status.HTTP_403_FORBIDDEN)

        try:
            a = self.get_queryset()
        except Exception as e:
            print e.message
            return Response({'error': 'Bad query'}, status.HTTP_400_BAD_REQUEST)
        if a:
            return Response(a)
        elif a is not None:
            return Response({'message': 'Filter did not match any item.'})

        app_names = {}

        for app in apps.get_app_configs():
            if getattr(app, 'analytics', False):
                app_names[app.name] = dict([(model.__name__, [field.name for field in model._meta.get_fields() if field.name in model.analytics_fields]) for model in app.get_models() if hasattr(model, 'analytics_fields')])

        return Response(app_names)
