import json
from random import randint

import time

import math
from django.test import TestCase
import requests

server_url = 'http://localhost:8080'
users_path = '/api/users/'

# User objects.
# Currently all user fields are mandatory.
unique_code = randint(0, 9999)
owner = {
    'first_name': 'Owner%i' % unique_code,
    'last_name':  'A',
    'username': 'owner_%i' % unique_code,
    'password': 'owner_%i' % unique_code,
    'email': 'owner_%i@mailinator.com' % unique_code,
    'is_owner': True,
    'is_employee': False,
    'is_customer': False
}

employee = {
    'first_name': 'Employee%i' % unique_code,
    'last_name':  'A',
    'username': 'employee_%i' % unique_code,
    'password': 'employee_%i' % unique_code,
    'email': 'employee_%i@mailinator.com' % unique_code,
    'is_owner': False,
    'is_employee': True,
    'is_customer': False
}
customer = {
    'first_name': 'Customer%i' % unique_code,
    'last_name':  'A',
    'username': 'customer_%i' % unique_code,
    'password': 'customer_%i' % unique_code,
    'email': 'customer_%i@mailinator.com' % unique_code,
    'is_owner': False,
    'is_employee': False,
    'is_customer': True
}


def user_creation(user):
    url = server_url + users_path
    r = requests.post(url, json=user)

    if r.status_code is 201:
        return json.loads(r.text)
    elif r.status_code == 400 and r.text.find(u'exists') > -1:
        return
    else:
        raise Exception(r.text)


## Run test
print ('CUSTOMER(S) CREATION')
print ('Create owner')
print (user_creation(owner))
print ('Groups are not created yet')
print ('Create employee')
print (user_creation(employee))
print ('Create customer')
print (user_creation(customer))
