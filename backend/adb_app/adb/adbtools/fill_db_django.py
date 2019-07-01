"""
Upload data via django interaction layer.
For now this must be executed interactively in the backend container.

"""

# TODO: create logging file (for bigg database for next release)
# TODO: colored logging

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

from pprint import pprint

import sqlite3
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from adb_app.adb.models import Collection, Evidence, Annotation, Mapping
from adb_app.adb.adbtools.fill_db_rest import get_identifiers_collections, BIGG_SQLITE3


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


def bigg_data_sources():
    """ Get the bigg data sources"""
    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()

    ns_replacements = {
        "mnx.chemical": "metanetx.chemical",
        "mnx.equation": "metanetx.equation",
        "ec": "ec-code",
        "REBASE": "rebase",
        "sabiork": "sabiork.reaction", # check
    }

    # data sources
    c.execute('''SELECT id, bigg_id, name, url_prefix FROM data_source''')
    all_rows = c.fetchall()
    data_sources = {}
    for row in all_rows:
        ns = row[1]

        # fix namespaces
        ns = ns_replacements.get(ns, ns)

        data_sources[row[0]] = {
            'pk': row[0],
            'namespace': ns,
            'name': row[2],
            'url_prefix': row[3],
        }

    db.close()
    return data_sources


def store_bigg_data_sources():
    data_sources = bigg_data_sources()
    for __, ds in data_sources.items():
        namespace = ds['namespace']
        try:
            collection = Collection.objects.get(namespace=namespace)
        except ObjectDoesNotExist:
            logging.warning(
                f"Bigg data_source missing: {namespace}"
            )

            # upload missing Bigg data resources
            name = ds['name']
            if not name:
                name = namespace

            collection = Collection(
                namespace=namespace,
                miriam=False,
                name=name,
                idpattern=".*",  # no restrictions
                urlpattern='{$id}'
            )
            collection.save()
            logging.info(collection)


def _store_annotation(collection, term):
    """ Store django annotation."""

    annotation = None
    try:
        annotation = Annotation(
            collection=collection,
            term=term
        )
        annotation.save()
    except ValidationError as err:
        if err != "{'__all__': ['Annotation with this Term and Collection already exists.']}":
            logging.error(err)
    return annotation


def store_bigg_annotations():
    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()

    print("*** reactions ***")
    collection = Collection.objects.get(namespace='bigg.reaction')
    c.execute('''SELECT id, bigg_id FROM reaction''')
    all_rows = c.fetchall()
    reactions = {}
    for row in all_rows:
        reactions[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'reaction'
        }
        _store_annotation(collection, term=row[1])

    print("*** compartments ***")
    collection = Collection.objects.get(namespace='bigg.compartment')
    c.execute('''SELECT id, bigg_id FROM compartment''')
    all_rows = c.fetchall()
    compartments = {}
    for row in all_rows:
        compartments[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'compartment'
        }
        _store_annotation(collection, term=row[1])

    print("*** metabolites ***")
    collection = Collection.objects.get(namespace='bigg.metabolite')
    c.execute('''SELECT id, bigg_id FROM component''')
    all_rows = c.fetchall()
    metabolites = {}
    for row in all_rows:
        metabolites[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'component'
        }
        _store_annotation(collection, term=row[1])

    db.close()
    return reactions, compartments, metabolites


def store_bigg_mappings():
    """ Upload all bigg annotations in database. """

    data_sources = bigg_data_sources()

    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()

    # get mappings
    c.execute('''SELECT id, ome_id, synonym, type, data_source_id FROM synonym''')

    all_rows = c.fetchall()
    for row in all_rows:

        term_target = row[2]
        synonym_type = row[3]
        data_source_id = row[4]

        if synonym_type in ["reaction", "component", "compartment"]:

            data_source = data_sources[data_source_id]
            bigg_ns = data_source["namespace"]

            # do not store the following synonyms
            if bigg_ns in ['old_bigg_id', 'deprecated']:
                continue

            # writing synonyms and mappings

            try:
                collection = Collection.objects.get(namespace=bigg_ns)

                # create target annotation
                annotation_target = _store_annotation(collection, term_target)
                if annotation_target is None:
                    logging.error('{0} : {1}, {2}'.format(row[0], row[1], row[2]))

            except ObjectDoesNotExist:
                logging.error(f"Target collection does not exist: {bigg_ns}")

            # TODO: create mapping between annotations

    db.close()


if __name__ == "__main__":
    # store_identifiers_collections()
    # store_bigg_evidence()
    # store_bigg_data_sources()
    # store_bigg_annotations()
    store_bigg_mappings()

