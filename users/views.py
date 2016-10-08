import random
import string
import uuid

from datetime import timedelta
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from rest_framework import status

from django.utils import timezone

from users.apps import CODE_EXPIRE_MIN, KEY_SIZE
from users.utils import send_mail
from .models import User, ForgotPassword
from djangae.contrib.gauth.datastore.models import Group
from .serializers import UserSerializer, GroupSerializer, ForgotPasswordSerializer, ForgotPasswordValidateSerializer, \
    ResetPasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ForgotPasswordViewSet(viewsets.ViewSet):
    """
    Handle the forgot password.
    """
    model = ForgotPassword
    serializer_class = ForgotPasswordSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Validate the user email exists and send the temporary recovery key

        :param request:
        :return:
        """
        form_data = ForgotPasswordSerializer(data=request.data)
        if not form_data.is_valid():
            return Response({'error': form_data.errors}, status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=form_data.validated_data.get('email'))
        except ObjectDoesNotExist:
            return Response({'error': 'Not found.'}, status.HTTP_404_NOT_FOUND)

        # Return the existing code if it already exists.
        exists = self.model.objects.filter(user_email=user.email,
                                           created_at__gte=timezone.now()-timedelta(minutes=CODE_EXPIRE_MIN),
                                           status=self.model.VALID)
        if exists and not exists[0].token:
            send_mail(exists[0].code, exists[0].user_email)
            return Response({'message': 'A key was sent to the user email.'})

        if exists and exists[0].token:
            exists.update(status=self.model.INVALID)

        # Create a new recovery code and show it to the user.
        recovery_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(KEY_SIZE))

        recovery = self.model(user=user, user_email=user.email, code=recovery_key)
        recovery.save()

        send_mail(recovery_key, user.email)

        return Response({'message': 'A key was sent to the user email.'})


class ForgotPasswordValidateViewSet(viewsets.ViewSet):
    """
    Handle the forgot password.
    """
    model = ForgotPassword
    serializer_class = ForgotPasswordValidateSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        """
        Validate the submitted code is valid.

        :param request:
        :return:
        """
        form_data = ForgotPasswordValidateSerializer(data=request.data)
        if not form_data.is_valid():
            return Response({'error': form_data.errors}, status.HTTP_400_BAD_REQUEST)

        # Validate the code exists
        try:
            recovery = self.model.objects.get(user_email=form_data.validated_data.get('email'),
                                              created_at__gte=timezone.now()-timedelta(minutes=CODE_EXPIRE_MIN))
        except self.model.DoesNotExist:
            return Response({'error': 'Not valid.'}, status.HTTP_400_BAD_REQUEST)

        # Create the temporary token
        token = uuid.uuid4()
        recovery.token = token
        recovery.save()

        return Response({'message': 'Key is valid.', 'token': token})


class ResetPasswordViewSet(viewsets.ViewSet):
        """
        Reset the password when .
        """
        model = ForgotPassword
        serializer_class = ResetPasswordSerializer
        permission_classes = [AllowAny]

        def create(self, request):
            """
            Validate the submitted code is valid.

            :param request:
            :return:
            """
            form_data = ResetPasswordSerializer(data=request.data)
            if not form_data.is_valid():
                return Response({'error': form_data.errors}, status.HTTP_400_BAD_REQUEST)

            recovery = self.model.objects.get(token=form_data.validated_data.get('token'))

            user = User.objects.get(pk=recovery.user_id)
            user.set_password(form_data.validated_data.get('new_password'))
            user.save()

            return Response({'message': 'Password updated.'})
