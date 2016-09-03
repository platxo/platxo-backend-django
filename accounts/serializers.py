from rest_framework import serializers

from django.contrib.auth.models import User

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'password', 'url')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    username=validated_data['username'],
                    email=validated_data['email']
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
