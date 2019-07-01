"""
Upload data via django interaction layer.
For now this must be executed interactively in the backend container.

"""
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'adb_app.settings'

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#sys.path.append(BASE_DIR)
#print(BASE_DIR)


from dotenv import load_dotenv
# OR, the same with increased verbosity:
env_path = os.path.abspath("../../../../.env.local")
print(env_path)
load_dotenv(dotenv_path=env_path, verbose=True)

import logging
import django
django.setup()

from django.core.exceptions import ObjectDoesNotExist

from adb_app.adb.models import Collection, Evidence
from adb_app.adb.adbtools.fill_db_rest import get_identifiers_collections


def store_identifiers_collections():
    # get latest identifiers.org collections
    json_dict = get_identifiers_collections()

    collections = []
    for entry in json_dict['payload']['namespaces']:
        namespace = entry['prefix']

        try:
            collection = Collection.objects.get(namespace=namespace)
            logging.warning(f"collection exists: {collection}")

        except ObjectDoesNotExist:
            collection = Collection(
                namespace=entry['prefix'],
                miriam=True,
                name=entry['name'],
                idpattern=entry['pattern'],
                urlpattern='https://identifiers.org/' + entry['prefix'] + '/{$id}'
            )
            collection.save()
            logging.info(collection)


def store_bigg_evidence():
    """

    :return:
    """
    # post evidence
    try:
        evidence = Evidence.objects.get(source="bigg", version="1.5")
        logging.warning(f"evidence exists: {evidence}")

    except ObjectDoesNotExist:
        evidence = Evidence(
            source="bigg",
            version="1.5",
            evidence="database"
        )
        evidence.save()
        logging.info(evidence)


if __name__ == "__main__":
    store_identifiers_collections()
    store_bigg_evidence()

