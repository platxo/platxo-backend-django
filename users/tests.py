import json
from random import randint

import time

import math
from django.test import TestCase
import requests

server_url = 'http://localhost:8080'
users_path = '/api/users/'
groups_path = '/api/groups/'
authentication_path = '/api-token-auth/'

# User objects.
# Currently all user fields are mandatory.
unique_code = randint(0, 9999)
OWNER = 'owner'
EMPLOYEE = 'employee'
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

group_names = ['customer', 'employee', 'owner']


def create_groups():
    """
    Create default groups, these groups are created only one, and require user authenticated.

    :return:
    """
    print ('Creating groups.')
    url = server_url + groups_path
    for group in group_names:
        requests.post(url, json={'name': group, 'permissions': []})


def user_creation(user):
    url = server_url + users_path
    r = requests.post(url, json=user)

    if r.status_code is 201:
        return json.loads(r.text)
    elif r.status_code == 400 and r.text.find(u'exists') > -1:
        return
    else:
        raise Exception(r.text)


def user_authentication():
    pass


def create_user(user_type):
    if user_type is 'owner':
        return user_creation(owner)
    elif user_type is 'employee':
        return user_creation(employee)
    elif user_type is 'customer':
        return user_creation(customer)
    else:
        raise (Exception('User type not supported'))


def create_all():
    create_groups()
    users = {}
    for user_type in ['owner', 'employee', 'customer']:
        print('Create %s' % user_type)
        users[type] = create_user(user_type)
        print(users[type].get('id'))
    return users


#####
if __name__ == '__main__':
    """
    Run test
    """
    print ('CUSTOMER(S) CREATION')
    create_all()
