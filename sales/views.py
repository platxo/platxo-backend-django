from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView

from business.models import Business
from .models import Sale, PurchaseOrder
from .serializers import SaleSerializer, OrderRequestSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class OrderPurchaseViewSet(viewsets.ViewSet):

    queryset = PurchaseOrder.objects.all()
    read_serializer = OrderRequestSerializer

    def get_queryset(self):
        """
        Business can see all purchases.
        Employee can see only those they generated.
        :return:
        """
        user = self.request.user
        query = {}
        if user.is_owner and user.owner.business:
            query = {'business__in': user.owner.business.all()}
        elif user.is_employee and user.employee:
            # Correct this
            # business_query = Business.objects.filter(employees__contains=user.employee)
            query = {'employee__in': user.employee.id}
        else:
            business_query = {'pk': None}
        return self.queryset.filter(**query) #business__in=business_query)

    def list(self, request):

        return Response(self.read_serializer(self.get_queryset(), many=True).data)

    def retrieve(self, request, pk=None):
        try:
            return Response(self.read_serializer(self.get_queryset().get(pk=pk)).data)
        except PurchaseOrder.DoesNotExist:
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

        order_serialized = OrderRequestSerializer(data=order)
        if not order_serialized.is_valid():
            return Response({'error': order_serialized.errors}, status=status.HTTP_400_BAD_REQUEST)

        order_saved = order_serialized.save()

        # Validate that
        return Response({'message': 'Order stored.', 'total': order_saved.total})
