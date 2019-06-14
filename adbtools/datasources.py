"""
Data source table

--------------------------------------------
pk, id, miriam, name, idpattern, urlpattern
--------------------------------------------

version data_source source_term qualifier



Additional bigg data sources
-----------------------------
slm
envipath
refseq_orf_id	RefSeq ORF ID
IMGT/GENE-DB
REBASE
refseq_old_locus_tag	RefSeq Old Locus Tag
refseq_locus_tag
refseq_name
EnsemblGenomes-Gn
EnsemblGenomes-Tr
PSEUDO



"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'adb_app.settings'
from dotenv import load_dotenv
load_dotenv(dotenv_path="../.env.local", verbose=True)

import django
django.setup()

import json
from pprint import pprint
from adb_app import settings

from adb_app.annotations.models import Collection


import os
import coloredlogs
import logging
import collections
import requests
from json.decoder import JSONDecodeError

from pkdb_data.management.envs import API_URL, API_BASE, USER, PASSWORD, DEFAULT_USER_PASSWORD
from pkdb_data.management.utils import read_json


# .env - environment variables
API_BASE = "http://0.0.0.0:9000"
USER = "admin"
PASSWORD = "adb_admin"




coloredlogs.install(fmt='%(levelname)s %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_authentication_headers(api_base, username, password):
    """ Get authentication header with token for given user.

    Returns admin authentication as default.
    """
    auth_token_url = os.path.join(api_base, "api-token-auth/")
    try:
        response = requests.post(auth_token_url, json={"username": username, "password": password})
    except requests.exceptions.ConnectionError as e:
        raise requests.exceptions.InvalidURL(f"Error Connecting (probably wrong url <{api_base}>): ", e)

    if response.status_code != 200:
        logging.error(f"Request headers could not be retrieved from: {auth_token_url}")
        logging.warning(response.text)
        raise requests.exceptions.ConnectionError(response)

    token = response.json().get("token")
    return {'Authorization': f'token {token}'}


def requests_with_client(client, requests, *args, **kwargs):
    method = kwargs.pop("method", None)

    if client:
        if kwargs.get("files"):
            kwargs["data"] = kwargs.pop("files", None)
            response = getattr(client, method)(*args, **kwargs)

        else:
            response = getattr(client, method)(*args, **kwargs, format='json')
    else:
        kwargs["json"] = kwargs.pop("data", None)
        response = getattr(requests, method)(*args, **kwargs)

    return response


def upload_choices(api_url, choice, auth_headers, data_json, client=None):
    for instance in data_json:
        response = requests_with_client(client, requests, f"{api_url}/{choice}/", method="post",
                                        data=instance, headers=auth_headers)

        if not response.status_code == 201:
            if response.json():
                instance_exists = any(["already exists" in values[0] for key, values in response.json().items()])

                if instance_exists:
                    continue

            logging.warning(f"{choice} upload failed: {instance} ")
            logging.warning(response.content)


def load_miriam():
    """ Loads miriam registry file.

    identifiers.org collection

    :return:
    """
    f_miriam = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '..', 'resources', 'miriam', 'identifiers_org_collections.json'
    )

    with open(f_miriam) as fp:
        d = json.load(fp)

    return d


def upload_miriam_collections():
    collections = []
    miriam_collections = load_miriam()
    for key, item in miriam_collections.items():
        print(key)
        collection = Collection(
            namespace=item['namespace'],
            miriam=True,
            idpattern=item['pattern'],
            urlpattern="https://identifiers.org/{id}"
        )
        collection.save()


    # Collection.objects.bulk_create(
    #     collections
    # )


if __name__ == "__main__":
    upload_miriam_collections()
