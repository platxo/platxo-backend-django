from django.contrib.auth.backends import ModelBackend
from django.conf import settings
from django.contrib.auth import get_user_model
# STANDARD LIB
from itertools import chain
# DJANGAE
from djangae.db import transaction
from djangae.contrib.gauth.datastore.permissions import get_permission_choices


"""  DEFAULT SETTINGS + ALIAS   """

try:
    am = settings.AUTHENTICATION_METHOD
except:
    am = 'both'
try:
    cs = settings.AUTHENTICATION_CASE_SENSITIVE
except:
    cs = 'both'


"""   EXCEPTIONS  """

VALID_AM = ['username', 'email', 'both']
VALID_CS = ['username', 'email', 'both', 'none']

if (am not in VALID_AM):
    raise Exception("Invalid value for AUTHENTICATION_METHOD in project "
                    "settings. Use 'username','email', or 'both'.")

if (cs not in VALID_CS):
    raise Exception("Invalid value for AUTHENTICATION_CASE_SENSITIVE in project "
                    "settings. Use 'username','email', 'both' or 'none'.")


"""  OVERRIDDEN METHODS  """



class UserBackend(ModelBackend):

    """
    This is a ModelBacked that allows authentication
    with either a username or an email address and use
    the permissions in grops.
    """

    def authenticate(self, username=None, password=None):
        UserModel = get_user_model()
        try:
            if ((am == 'email') or (am == 'both')):
                if ((cs == 'email') or cs == 'both'):
                    kwargs = {'email': username}
                else:
                    kwargs = {'email__iexact': username}

                user = UserModel.objects.get(**kwargs)
            else:
                raise
        except:
            if ((am == 'username') or (am == 'both')):
                if ((cs == 'username') or cs == 'both'):
                    kwargs = {'username': username}
                else:
                    kwargs = {'username__iexact': username}

                user = UserModel.objects.get(**kwargs)
        finally:
            try:
                if user.check_password(password):
                    return user
            except:
                # Run the default password hasher once to reduce the timing
                # difference between an existing and a non-existing user.
                UserModel().set_password(password)
                return None

    def get_user(self, username):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=username)
        except UserModel.DoesNotExist:
            return None



    atomic = transaction.atomic
    atomic_kwargs = {'xg': True}

    def get_group_permissions(self, user_obj, obj=None):
        """
        Returns a set of permission strings that this user has through his/her
        groups.
        """
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_group_perm_cache'):
            if user_obj.is_superuser:
                perms = (perm for perm, name in get_permission_choices())
            else:
                perms = chain.from_iterable((group.permissions for group in user_obj.groups.all()))
            user_obj._group_perm_cache = set(perms)
        return user_obj._group_perm_cache

    def get_all_permissions(self, user_obj, obj=None):
        if user_obj.is_anonymous() or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = set(user_obj.user_permissions)
            user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        return user_obj._perm_cache
