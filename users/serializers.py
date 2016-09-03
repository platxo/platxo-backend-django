from rest_framework import serializers

from .models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = (
                  'id',
                  'is_owner',
                  'is_employed',
                  'is_customer',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
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
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


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
