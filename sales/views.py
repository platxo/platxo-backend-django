from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from .models import Sale
from .serializers import SaleSerializer, OrderRequestSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class OrderPurchaseViewSet(viewsets.ViewSet):

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

        order_serialized = OrderRequestSerializer(data=order)
        if not order_serialized.is_valid():
            return Response({'error': order_serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

        order_saved = order_serialized.save()

        # Validate that
        return Response({'message': 'Order stored.', 'total': order_saved.total})
