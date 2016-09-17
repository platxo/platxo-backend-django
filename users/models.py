from __future__ import unicode_literals

from django.db import models
# DJANGO
from django.contrib.auth.models import UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.validators import ASCIIUsernameValidator, UnicodeUsernameValidator
from django.core.mail import send_mail
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
# DJANGAE
from djangae.contrib.gauth.datastore.models import PermissionsMixin


class AbstractUser(AbstractBaseUser, PermissionsMixin):

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
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    is_owner = models.BooleanField(
        _('is owner'),
        default=False,
        help_text=_(
            'Designates whether this user is owner. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_employee = models.BooleanField(
        _('is employee'),
        default=False,
        help_text=_(
            'Designates whether this user is employee. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_customer = models.BooleanField(
        _('is customer'),
        default=False,
        help_text=_(
            'Designates whether this user is customer. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_supplier = models.BooleanField(
        _('is supplier'),
        default=False,
        help_text=_(
            'Designates whether this user is supplier. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    def get_owner_profile(self):
        owner_profile = None
        if hasattr(self, 'ownerprofile'):
            owner_profile = self.ownerprofile
        return owner_profile

    def get_employee_profile(self):
        employee_profile = None
        if hasattr(self, 'employeeprofile'):
            employee_profile = self.employeeprofile
        return employee_profile

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

    class Meta(AbstractUser.Meta):
        app_label = "users"
        swappable = 'AUTH_USER_MODEL'
