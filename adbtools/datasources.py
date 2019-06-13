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
        collections.append(
            Collection(
                namespace=item['namespace'],
                miriam=True,
                idpattern=item['pattern'],
                urlpattern="https://identifiers.org/{id}"
            )
        )
    Collection.objects.bulk_create(
        collections
    )


if __name__ == "__main__":
    upload_miriam_collections()
