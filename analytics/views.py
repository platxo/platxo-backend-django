from django.apps import apps
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from business.models import Business


class AnalyticsTest(viewsets.ViewSet):

    def get_queryset(self):
        """
        Get the specified fields from the specified model.
        :return:
        """
        app = self.request.query_params.get('app')
        model = self.request.query_params.get('model')
        field = self.request.query_params.get('field')
        fields = self.request.query_params.getlist('fields[]')

        business = self.request.user.owner.business.all()

        if app and model:
            a = apps.get_app_config(app).get_model(model)
            if not hasattr(a, 'analytics_fields'):
                # The model must be analytics eligible
                raise Exception('Incorrect model name.')
            if field:
                if field not in a.analytics_fields:
                    # The field is not parametrized in analytics_fields
                    raise Exception('Wrong field choice.')
                query_fields = list(field)
            elif fields:
                for value in fields:
                    if value not in a.analytics_fields:
                        # The field is not parametrized in analytics_fields
                        raise Exception('Wrong field choice.')
                query_fields = fields
            else:
                return a.objects.filter(business__in=business).values(*a.analytics_fields)

            filter_fields = dict([(field, self.request.query_params.get(field)) for field in query_fields if self.request.query_params.get(field, None)])

            return a.objects.all().filter(business__in=business, **filter_fields).values(*query_fields)

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
