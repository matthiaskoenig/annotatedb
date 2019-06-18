"""
ORM mapping for annotated bee.
"""
import os
import json
import logging
import requests

from adbtools.data import EVIDENCES, COLLECTIONS, ANNOTATIONS

# ------------------------------------------------------------
# Authentication
# ------------------------------------------------------------
'''
Test JWT authentication

curl -X POST -H "Content-Type: application/json" -d '{"username": "admin", "password": "adb_admin"}' http://localhost:9000/api/token/
'''

API_URL_BASE = "http://localhost:9000/"
REST_URL_BASE = API_URL_BASE + "api/v1/"

USER = "admin"
PASSWORD = "adb_admin"


def get_authentication_headers(api_base, username, password):
    """ Get authentication header with token for given user.

    """
    jwt_token_url = "{}api/token/".format(api_base)
    response = requests.post(jwt_token_url, json={"username": username, "password": password})

    if response.status_code != 200:
        logging.error(f"JWT token could not be retrieved from: {jwt_token_url}")
        logging.warning(response.text)
        raise requests.exceptions.ConnectionError(response)

    json_data = response.json()
    access = json_data.get('access')
    refresh = json_data.get('refresh')

    return {'Authorization': f'Bearer {access}'}


HEADERS = get_authentication_headers(
        api_base=API_URL_BASE,
        username=USER,
        password=PASSWORD
)


def _request(method, url, **kwargs):
    response = requests.request(method=method, url=url, **kwargs)

    if response.status_code in [200, 201]:
        return json.loads(response.content.decode('utf-8'))
    else:
        logging.error(response.status_code)
        logging.error(url)
        logging.error(response.text)
        return None


# ------------------------------------------------------------
# ORM mapping
# ------------------------------------------------------------
class Collection(object):
    __slots__ = ('namespace', 'miriam', 'name', 'idpattern', 'urlpattern')

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @staticmethod
    def post(data_dict):
        return _request(method="post",
                        url='{}collections/'.format(REST_URL_BASE),
                        headers=HEADERS,
                        json=data_dict)

    @staticmethod
    def get(namespace):
        return _request(
            method="get",
            url='{}collections/{}/'.format(REST_URL_BASE, namespace)
        )

    @staticmethod
    def get_all():
        # FIXME: get complete list
        return _request(
            method="get",
            url='{}collections/'.format(REST_URL_BASE)
        )


class Evidence(object):
    __slots__ = ('namespace', 'miriam', 'name', 'idpattern', 'urlpattern')

    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @staticmethod
    def post(data_dict):
        return _request(method="post",
                        url='{}collections/'.format(REST_URL_BASE),
                        headers=HEADERS,
                        json=data_dict)

    @staticmethod
    def get(namespace):
        return _request(
            method="get",
            url='{}collections/{}/'.format(REST_URL_BASE, namespace)
        )

    @staticmethod
    def get_all():
        # FIXME: get complete list
        return _request(
            method="get",
            url='{}collections/'.format(REST_URL_BASE)
        )



if __name__ == "__main__":

    # upload collections
    for collection in COLLECTIONS:
        Collection.post(data_dict=collection)

    c_sbo = Collection.get('sbo')
    print(c_sbo)

    c_all = Collection.get_all()
    print(c_all)





