from django.shortcuts import render
from django.views.generic import TemplateView

from google.appengine.api import app_identity
from google.appengine.api import mail

from django.core.mail import send_mail


class IndexView(TemplateView):
    template_name = 'index.html'
