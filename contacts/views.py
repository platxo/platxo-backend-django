from django.shortcuts import render
from rest_framework import viewsets

from .models import Contact, Promotion
from .serializers import ContactSerializer, PromotionSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
