"""
Scripts for recreating the database.

Upload data via django interaction layer.
For now this must be executed interactively in the backend container.

Steps:
[1] update version numbers
- .env.local
- backend/adb_app/_version.py

[2] purge database
set -a && source .env.local
echo $ADB_VERSION
./docker-purge.sh

[3] execute this script in docker container (check log file)
docker exec -it adb_backend bash
root@76d113208c20:/# cd adb_app/adb/adbtools/
root@76d113208c20:/# python fill_db_django.py

[4] create materialized views
./adb_views.sh

[5] store database
./adb_dump.sh

"""
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'adb_app.settings'

import coloredlogs
import logging

logFormatter = logging.Formatter("[%(levelname)s]  %(message)s")
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler("{0}/{1}.log".format('.', 'bigg-v1.5-mapping'), 'w+')
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.WARNING)

coloredlogs.install(fmt='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

import django
django.setup()

import re
import sqlite3
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.utils import IntegrityError

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

    try:
        annotation = Annotation.objects.get(
            collection=collection, term=term
        )
    except ObjectDoesNotExist:
        try:
            annotation = Annotation(
                collection=collection,
                term=term
            )
            annotation.save()
        except ValidationError as err:
            logging.error(err.message_dict)
            return None

    return annotation


def bigg_reactions():
    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()
    c.execute('''SELECT id, bigg_id FROM reaction''')
    all_rows = c.fetchall()
    data = {}
    for row in all_rows:
        data[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'reaction'
        }
    db.close()
    return data


def bigg_compartments():
    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()
    c.execute('''SELECT id, bigg_id FROM compartment''')
    all_rows = c.fetchall()
    data = {}
    for row in all_rows:
        data[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'compartment'
        }
    db.close()
    return data


def bigg_metabolites():
    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()
    c.execute('''SELECT id, bigg_id FROM component''')
    all_rows = c.fetchall()
    data = {}
    for row in all_rows:
        data[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'component'
        }
    db.close()
    return data


def store_bigg_annotations():
    print("*** reactions ***")
    reactions = bigg_reactions()
    collection = Collection.objects.get(namespace='bigg.reaction')
    for item in reactions.values():
        _store_annotation(collection, term=item['bigg_id'])

    print("*** compartments ***")
    compartments = bigg_compartments()
    collection = Collection.objects.get(namespace='bigg.compartment')
    for item in compartments.values():
        _store_annotation(collection, term=item['bigg_id'])

    print("*** metabolites ***")
    metabolites = bigg_metabolites()
    collection = Collection.objects.get(namespace='bigg.metabolite')
    for item in metabolites.values():
        _store_annotation(collection, term=item['bigg_id'])

    return reactions, compartments, metabolites


def store_bigg_mappings():
    """ Upload all bigg annotations in database. """

    # data for lookup
    data_sources = bigg_data_sources()
    reactions = bigg_reactions()
    compartments = bigg_compartments()
    metabolites = bigg_metabolites()

    bigg_collections = {
        "bigg.reaction": Collection.objects.get(namespace="bigg.reaction"),
        "bigg.metabolite": Collection.objects.get(namespace="bigg.metabolite"),
        "bigg.compartment": Collection.objects.get(namespace="bigg.compartment"),
    }

    bigg_db_evidence = Evidence.objects.get(
        source="bigg",
        version="1.5",
        evidence="database"
    )

    # get mappings
    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()
    c.execute(
        '''SELECT id, ome_id, synonym, type, data_source_id FROM synonym'''
    )
    all_rows = c.fetchall()

    for row in all_rows:

        term_target = row[2]
        synonym_type = row[3]
        data_source_id = row[4]

        if synonym_type in ["reaction", "component", "compartment"]:

            # resolve data source
            data_source = data_sources[data_source_id]
            bigg_ns = data_source["namespace"]

            # do not store the following synonyms
            if bigg_ns in ['old_bigg_id', 'deprecated']:
                continue

            # get source bigg annotation
            if synonym_type == "reaction":
                collection_str = "bigg.reaction"
                term_source = reactions[row[1]]['bigg_id']
            elif synonym_type == "component":
                collection_str = "bigg.metabolite"
                term_source = metabolites[row[1]]['bigg_id']
            elif synonym_type == "compartment":
                collection_str == "bigg.metabolite"
                term_source = compartments[row[1]]['bigg_id']
            collection_source = bigg_collections[collection_str]
            annotation_source = Annotation.objects.get(
                term=term_source, collection=collection_source
            )

            # perform identifier fixes
            term_target_fix = term_target
            if bigg_ns == "reactome":
                # missing R-ALL- prefixes
                p = re.compile('\d+')
                m = p.match(term_target)
                if m:
                    term_target_fix = f"R-ALL-{term_target}"
                    logging.warning(f"Fixing reactome prefix: {term_target} -> {term_target_fix}")


                # incorrect REACT_R prefixes
                elif term_target.startswith("REACT_R-"):
                    term_target_fix = term_target[6:]
                    logging.warning(f"Fixing reactome prefix: {term_target} -> {term_target_fix}")

            elif bigg_ns == "kegg.compound":
                # glycans incorrect as kegg.compounds
                p = re.compile('^G\d+$')
                m = p.match(term_target)
                if m:
                    logging.warning(f"Fixing collection kegg.compound -> kegg.glycan: {term_target}")
                    bigg_ns = "kegg.glycan"

            elif bigg_ns in ["kegg.reaction", "rhea", "sabiork.reaction"]:
                # incorrect #1 or #2 endings
                if term_target.endswith("#1") or term_target.endswith("#2"):
                    term_target_fix = term_target[:-2]
                    logging.warning(
                        f"Fixing incorrect ending ({bigg_ns}): {term_target} -> {term_target_fix}")

            elif bigg_ns == "ec-code":
                # ec-code to short, e.g. 1.2.1 -> 1.2.1.-
                p = re.compile(r"^\d+\.\d+\.\d+$")
                m = p.match(term_target)
                if m:
                    term_target_fix = f"{term_target}.-"
                    logging.warning(
                        f"Fixing ec-code: {term_target} -> {term_target_fix}"
                    )
                # ec-code to short, e.g. 1.2 -> 1.2.-.-
                p = re.compile(r"^\d+\.\d+$")
                m = p.match(term_target)
                if m:
                    term_target_fix = f"{term_target}.-.-"
                    logging.warning(
                        f"Fixing ec-code: {term_target} -> {term_target_fix}"
                    )

            # writing synonyms and mappings
            try:
                collection_target = Collection.objects.get(namespace=bigg_ns)

                # create target annotation
                annotation_target = _store_annotation(
                    collection_target, term_target_fix
                )

                if annotation_target is not None:
                    try:
                        mapping = Mapping(
                            source=annotation_source,
                            qualifier=Mapping.IS,
                            target=annotation_target,
                            evidence=bigg_db_evidence
                        )
                        mapping.save()
                    except IntegrityError as err:
                        logging.error(err)

            except ObjectDoesNotExist:
                logging.error(f"Target collection does not exist: {bigg_ns}")

    db.close()


if __name__ == "__main__":
    store_identifiers_collections()
    store_bigg_evidence()
    store_bigg_data_sources()
    store_bigg_annotations()
    store_bigg_mappings()

