from rest_framework import serializers

from .models import User
from business.models import Business
from djangae.contrib.gauth.datastore.models import Group
from django.contrib.auth.models import Permission
from rest_framework.reverse import reverse


class UserSerializer(serializers.HyperlinkedModelSerializer):
    is_owner = serializers.BooleanField(default=False)
    is_employed = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    is_supplier = serializers.BooleanField(default=False)
    business = serializers.SerializerMethodField()

    def get_business(self, foo):
        if foo.is_owner:
            return [busi.pk for busi in Business.objects.filter(owner=foo.owner)]
        if foo.is_employed:
            return [busi.pk for busi in Business.objects.filter(employees__contains=foo.employed)]
        else:
            return None



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
                  'business',
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

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.HyperlinkedRelatedField(
        many=True,
        queryset=Permission.objects.all(),
        view_name='permission-detail'
    )
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
