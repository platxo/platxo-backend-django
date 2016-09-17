from rest_framework import serializers

from business.models import Business


class OneProductOrService(object):
    """
    Ensure at least one product or service comes.
    """
    def __init__(self):
        pass

    def __call__(self, attrs):
        if not attrs.get('products') and not attrs.get('services'):
            raise serializers.ValidationError("Include at least one product or service.")


class UserInBusiness(object):
    """
    Validate  that employee and customer belongs to the business.
    """
    def __init__(self, field, anonymous=False):
        self.field = field
        self.anonymous = anonymous

    def __call__(self, attrs):
        if self.anonymous and not attrs.get(self.field):
            return
        try:
            query_args = {'pk': attrs['business'].id, self.field + 's__contains': attrs[self.field]}
            if not Business.objects.filter(**query_args).exists():
                raise serializers.ValidationError({self.field: "{field} does not belong to Business".format(field=self.field)})

        except serializers.ValidationError as e:
            raise serializers.ValidationError(e.detail)
        except Exception as e:
            print e
            raise serializers.ValidationError(e.message)

        attrs[self.field + '_username'] = attrs[self.field].user.username
