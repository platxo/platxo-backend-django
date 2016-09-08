from rest_framework import serializers

from business.models import Business
from .models import User
from djangae.contrib.gauth.datastore.models import Group
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    is_owner = serializers.BooleanField(default=False)
    is_employed = serializers.BooleanField(default=False)
    is_customer = serializers.BooleanField(default=False)
    is_supplier = serializers.BooleanField(default=False)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    business = serializers.SerializerMethodField()

    def get_business(self, user):
        if user.is_owner:
            return [business.pk for business in Business.objects.filter(owner=user.owner)]
        if user.is_employed:
            return [business.pk for business in Business.objects.filter(employees__contains=user.employed)]
        if user.is_customer:
            return [business.pk for business in Business.objects.filter(customers__contains=user.customer)]
        if user.is_supplier:
            return [business.pk for business in Business.objects.filter(suppliers__contains=user.supplier)]
        else:
            return None

    class Meta:
        model = User
        fields = (
                  'id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'is_owner',
                  'is_employed',
                  'is_customer',
                  'is_supplier',
                  'owner',
                  'employed',
                  'customer',
                  'supplier',
                  'business',
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
