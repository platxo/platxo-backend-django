from datetime import datetime
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from business.models import Business
from .models import Sale, Sale
from .serializers import SaleSerializer



class SaleViewSet(viewsets.ViewSet):

    queryset = Sale.objects.all()
    read_serializer = SaleSerializer

    def get_queryset(self):
        """
        Business can see all purchases.
        Employee can see only those they generated.
        :return:
        """
        user = self.request.user
        if user.is_owner and user.owner.business:
            query = {'business__in': user.owner.business.all()}
        elif user.is_employee and user.employee:
            query = {'employee': user.employee}
        else:
            query = {'pk': None}
        return self.queryset.filter(**query)

    def default_date_filter(self):
        """
        Returns the purchases made in the last month, according to application default behaviour.
        :return:
        """
        now = datetime.now()
        next_month = datetime(now.year, now.month+1, 1)
        return {'created_at__gte': '{year}-{month}-01'.format(year=now.year, month=now.month),
                'created_at__lt': '{year}-{month}-01'.format(year=next_month.year, month=next_month.month)}

    def list(self, request):
        """
        Show all purchases made.
        :param request:
        :return:
        """
        return Response(self.read_serializer(self.get_queryset().filter(**self.default_date_filter()), many=True).data)

    def retrieve(self, request, pk=None):
        try:
            return Response(self.read_serializer(self.get_queryset().get(pk=pk)).data)
        except Sale.DoesNotExist:
            return Response({'Error': 'Sale not found.'}, status.HTTP_404_NOT_FOUND)

    def create(self, request, format=None):
        """
        Handles the purchase of products and services.

        Serializer:
            order
               payment_method ((str)ex. cash, credit card)
               products[{qty, id, discount}]
               employee (id)
               business (id)

        :param request:
        :param format:
        :return:
        """
        order = request.data.get('order')

        if not order:
            return Response({'error': 'Missing order field.'}, status=status.HTTP_400_BAD_REQUEST)

        order_serialized = SaleSerializer(data=order)
        if not order_serialized.is_valid():
            return Response({'error': order_serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

        order_saved = order_serialized.save()

        return Response({'message': 'Order stored.',
                         'name': order_saved.name,
                         'subtotal': order_saved.subtotal,
                         'tax': order_saved.total_taxes,
                         'discount': order_saved.total_discount,
                         'customer_point': order_saved.customer_points,
                         'total': order_saved.total})

    def update(self, request, pk=None):
        """
        Updated purchase order.

        It cancels the original order and creates a new one.

        :param request:
        :param pk:
        :return:
        """
        # if True:
        #     return Response({'message', 'Not implemented'}, status=status.HTTP_501_NOT_IMPLEMENTED)
        try:
            original_order = Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            return Response({'error': 'Order does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        order = request.data.get('order')

        if not order:
            return Response({'error': 'Missing order field.'}, status=status.HTTP_400_BAD_REQUEST)

        order_serialized = SaleSerializer(original_order, data=order, partial=True)
        if not order_serialized.is_valid():
            return Response({'error': order_serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

        order_serialized.update()

        return Response({'message': 'Order updated.', 'total': 0})

    def delete(self, request, pk=None):
        """
        Cancels the requested sale object.

        :param request:
        :param pk:
        :return:
        """
        try:
            original_order = Sale.objects.get(pk=pk)
        except Sale.DoesNotExist:
            return Response({'error': 'Order does not exists.'}, status=status.HTTP_400_BAD_REQUEST)

        order_serialized = SaleSerializer(original_order)

        try:
            order_serialized.delete()
        except Exception as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': "Sale cancelled"})
