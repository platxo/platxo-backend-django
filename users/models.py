from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from djangae.contrib.gauth.datastore.models import GaeAbstractDatastoreUser
from django.utils import six
from django.utils.translation import ugettext_lazy as _


class User(GaeAbstractDatastoreUser):
    username_validator = UnicodeUsernameValidator() if six.PY3 else ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=True)
    is_owner = models.BooleanField(default=False)
    is_employed = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)

    def get_owner_profile(self):
        owner_profile = None
        if hasattr(self, 'ownerprofile'):
            owner_profile = self.ownerprofile
        return owner_profile

    def get_employed_profile(self):
        employed_profile = None
        if hasattr(self, 'employedprofile'):
            employed_profile = self.employedprofile
        return employed_profile

    def get_customer_profile(self):
        customer_profile = None
        if hasattr(self, 'customerprofile'):
            customer_profile = self.customerprofile
        return customer_profile

    def get_supplier_profile(self):
        supplier_profile = None
        if hasattr(self, 'supplierprofile'):
            supplier_profile = self.supplierprofile
        return supplier_profile

    class Meta:
        app_label = "users"
        swappable = 'AUTH_USER_MODEL'
        verbose_name = _('user')
        verbose_name_plural = _('users')
