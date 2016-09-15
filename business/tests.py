import json
from random import randint

import requests
from django.test import TestCase

from users.tests import create_all, create_user, OWNER, EMPLOYEE

server_url = 'http://localhost:8080'
business_path = '/api/business/'

unique_code = randint(0, 9999)
business = {
    'owner': None,
    'name': 'Business %i' % unique_code,
    'employees': [],
    'customers': [],
    'suppliers': []

}


def create_business(user):
    # The business must be created with the user.owner table id
    business['owner'] = user['owner']
    url = server_url + business_path

    r = requests.post(url, json=business)

    if r.status_code == 201:
        return json.loads(r.text)
    elif r.status_code == 400 and r.text.find(u'exists') > -1:
        return
    else:
        raise Exception(r.text)


def add_employee_to_business(busi, user):
    busi['employees'].append(user['employee'])
    url = server_url + business_path + str(busi['id']) + '/'

    r = requests.put(url, json=busi)
    if r.status_code == 200:
        return json.loads(r.text)
    else:
        raise Exception(r.text)


def default_business_creation():
    owner = create_user(OWNER)
    print owner
    busi = create_business(owner)
    employee = create_user(EMPLOYEE)
    add_employee_to_business(busi, employee)


#####
if __name__ == '__main__':
    """
    Run test
    """
    default_business_creation()
