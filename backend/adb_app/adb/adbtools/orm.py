"""
ORM mapping for annotated bee.
"""
import json
import logging
import requests

from backend.adb_app.adb.adbtools.data import EVIDENCES, COLLECTIONS, ANNOTATIONS

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

class Base(object):
    def __getitem__(self, key):
        return getattr(self, key)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @staticmethod
    def post(infix, data_dict):
        return _request(method="post",
                        url='{}{}/'.format(REST_URL_BASE, infix),
                        headers=HEADERS,
                        json=data_dict)

    @staticmethod
    def get(infix, key):
        return _request(
            method="get",
            url='{}{}/{}/'.format(REST_URL_BASE, infix, key)
        )

    @staticmethod
    def get_all(infix):
        # FIXME: get complete list
        return _request(
            method="get",
            url='{}{}/'.format(REST_URL_BASE, infix)
        )


class Collection(Base):
    __slots__ = ('namespace', 'miriam', 'name', 'idpattern', 'urlpattern')
    __infix = 'collections'

    @classmethod
    def post(cls, data_dict):
        return Base.post(infix=cls.__infix, data_dict=data_dict)

    @classmethod
    def get(cls, key):
        return Base.get(infix=cls.__infix, key=key)

    @classmethod
    def get_all(cls):
        return Base.get_all(infix=cls.__infix)


class Evidence(Base):
    __slots__ = ('source', 'version', 'evidence')
    __infix = 'evidences'

    @classmethod
    def post(cls, data_dict):
        return Base.post(infix=cls.__infix, data_dict=data_dict)

    @classmethod
    def get(cls, key):
        return Base.get(infix=cls.__infix, key=key)

    @classmethod
    def get_all(cls):
        return Base.get_all(infix=cls.__infix)


class Annotation(Base):
    __slots__ = ('term', 'collection')
    __infix = 'annotations'

    @classmethod
    def post(cls, data_dict):
        return Base.post(infix=cls.__infix, data_dict=data_dict)

    @classmethod
    def get(cls, key):
        return Base.get(infix=cls.__infix, key=key)

    @classmethod
    def get_all(cls):
        return Base.get_all(infix=cls.__infix)


if __name__ == "__main__":

    # upload collections
    for collection in COLLECTIONS:
        Collection.post(data_dict=collection)

    for evidence in EVIDENCES:
        Evidence.post(data_dict=evidence)

    for annotation in ANNOTATIONS:
        Annotation.post(data_dict=annotation)



    c_sbo = Collection.get('sbo')
    print(c_sbo)
    c_all = Collection.get_all()
    print(c_all)

    e1 = Evidence.get('1')
    print(e1)
    e_all = Evidence.get_all()
    print(e_all)

    a1 = Annotation.get('1')
    print(a1)
    a_all = Annotation.get_all()
    print(a_all)





