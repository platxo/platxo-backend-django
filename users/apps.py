from __future__ import unicode_literals

from django.apps import AppConfig

KEY_SIZE = 6
CODE_EXPIRE_MIN = 180
TOKEN_EXPIRE_MIN = 15


class UsersConfig(AppConfig):
    name = 'users'
