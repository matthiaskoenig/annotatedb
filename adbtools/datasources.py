"""
Data source table

"""
import os
# os.environ['DJANGO_SETTINGS_MODULE'] = 'adb_app.settings'

import logging
# import django
# django.setup()

import json
#from adb_app.annotations.models import Collection

import requests

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


def get_identifiers():
    response = requests.get("https://registry.api.identifiers.org/resolutionApi/getResolverDataset")
    if response.status_code != 200:
        logging.error(response.status_code)
        logging.error(response.text)

    return response.json()



if __name__ == "__main__":
    # get latest identifiers.org collections
    json_dict = get_identifiers()
    with open("./identifiers.json", 'w') as f:
        json.dump(json_dict, f, indent=2)

    exit()



    # upload_miriam_collections()
