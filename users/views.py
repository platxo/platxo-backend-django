from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .models import User
from djangae.contrib.gauth.datastore.models import Group
from .serializers import UserSerializer, GroupSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
