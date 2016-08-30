"""
WSGI config for platxo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
from djangae.wsgi import DjangaeApplication

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "platxo.settings")

application = DjangaeApplication(get_wsgi_application())
