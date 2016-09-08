from rest_framework import serializers

from .models import User
from djangae.contrib.gauth.datastore.models import Group
from django.contrib.auth.models import Permission




class UserSerializer(serializers.ModelSerializer):
    is_owner = serializers.BooleanField(default=False)
    is_employed = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    is_supplier = serializers.BooleanField(default=False)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())

    class Meta:
        model = User
        fields = (
                  'id',
                  'is_owner',
                  'is_employed',
                  'is_customer',
                  'is_supplier',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'owner',
                  'employed',
                  'customer',
                  'supplier',
                  'groups',
                  'password',
                  'url'
                  )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    username=validated_data['username'],
                    email=validated_data['email'],
                    is_owner=validated_data['is_owner'],
                    is_employed=validated_data['is_employed'],
                    is_customer=validated_data['is_customer'],
                    is_supplier=validated_data['is_supplier'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions', 'url')


def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.
    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request},).data
    }
