from django.apps import apps
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status


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

        if app and model:
            a = apps.get_app_config(app).get_model(model).objects.all()
            if field:
                a = a.values(field)
            elif fields:
                a = a.values(*fields)
            else:
                a = a.values()
            return a

    def list(self, request):
        """
        Return the available operations or the requested information.

        Note: An application to be eligible in the analytics module must have its apps.AppConfig.analytics=True
        :param request:
        :return:
        """
        try:
            a = self.get_queryset()
        except Exception:
            return Response({'error': 'Bad query'}, status.HTTP_400_BAD_REQUEST)
        if a:
            return Response(a)

        app_names = {}

        for app in apps.get_app_configs():
            if getattr(app, 'analytics', False):
                app_names[app.name] = dict([(model.__name__, [field.name for field in model._meta.get_fields()]) for model in app.get_models()])

        return Response(app_names)
