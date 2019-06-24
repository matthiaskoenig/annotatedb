import sqlite3
import json
import requests

from adbtools.annotatedb import Collection, Evidence, Annotation


BIGG_SQLITE3 = '../bigg/bigg-v1.5.sqlite3'


def get_identifiers_collections():
    response = requests.get("https://registry.api.identifiers.org/resolutionApi/getResolverDataset")
    if response.status_code != 200:
        return None

    return response.json()


def post_identifiers_collections():
    # get latest identifiers.org collections
    json_dict = get_identifiers_collections()
    with open("./identifiers.json", 'w') as f:
        json.dump(json_dict, f, indent=2)

    for entry in json_dict['payload']['namespaces']:
        # print(entry)
        print(entry['prefix'])
        Collection.post(
            {
                "namespace": entry['prefix'],
                "miriam": True,
                "name": entry['name'],
                "idpattern": entry['pattern'],
                "urlpattern": 'https://identifiers.org/' + entry['prefix'] + '/{$id}',
            }
        )


def post_bigg_evidence():
    """
    Additional bigg collections

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

    :return:
    """

    # post additional collections
    bigg_collections = [

    ]

    # post evidence
    bigg_evidence = {
        "source": "bigg",
        "version": "1.5",
        "evidence": "database"
    }
    Evidence.post(data_dict=bigg_evidence)
    print(bigg_evidence)

    # post all annotations and mappings
    # bigg -> other resource


def post_bigg_annotations():
    db = sqlite3.connect('../bigg/bigg-v1.5.sqlite3')
    c = db.cursor()

    # data sources
    c.execute('''SELECT id, bigg_id, name, url_prefix FROM data_source''')
    all_rows = c.fetchall()
    data_sources = {}
    for row in all_rows:
        data_sources[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'name': row[2],
            'url_prefix': row[3],
        }

    print(data_sources)

    # reaction ids
    c.execute('''SELECT id, bigg_id FROM reaction''')
    all_rows = c.fetchall()
    reaction_ids = {}
    for row in all_rows:
        reaction_ids[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'reaction'
        }
        Annotation.post(data_dict={
            'collection': 'bigg.reaction',
            'term': row[1],
        })

    print(reaction_ids)

    # compartment ids
    c.execute('''SELECT id, bigg_id FROM compartment''')
    all_rows = c.fetchall()
    compartment_ids = {}
    for row in all_rows:
        compartment_ids[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'compartment'
        }
        Annotation.post(data_dict={
            'collection': 'bigg.compartment',
            'term': row[1],
        })
    print(compartment_ids)

    # metabolite/component ids
    c.execute('''SELECT id, bigg_id FROM component''')
    all_rows = c.fetchall()
    component_ids = {}
    for row in all_rows:
        component_ids[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'component'
        }
        Annotation.post(data_dict={
            'collection': 'bigg.metabolite',
            'term': row[1],
        })

    print(component_ids)

    db.close()
    return reaction_ids, compartment_ids, component_ids


def bigg_mappings():

    db = sqlite3.connect(BIGG_SQLITE3)
    c = db.cursor()

    # data sources
    c.execute('''SELECT id, bigg_id, name, url_prefix FROM data_source''')
    all_rows = c.fetchall()
    data_sources = {}
    for row in all_rows:
        data_sources[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'name': row[2],
            'url_prefix': row[3],
        }

    # reaction ids
    c.execute('''SELECT id, bigg_id FROM reaction''')
    all_rows = c.fetchall()
    reaction_ids = {}
    for row in all_rows:
        reaction_ids[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'reaction'
        }

    # compartment ids
    c.execute('''SELECT id, bigg_id FROM compartment''')
    all_rows = c.fetchall()
    compartment_ids = {}
    for row in all_rows:
        compartment_ids[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'compartment'
        }

    # print(compartment_ids)

    # metabolite/component ids
    c.execute('''SELECT id, bigg_id FROM component''')
    all_rows = c.fetchall()
    component_ids = {}
    for row in all_rows:
        component_ids[row[0]] = {
            'id': row[0],
            'bigg_id': row[1],
            'type': 'component'
        }
        #Annotation.post(data_dict={
        #    'collection': 'bigg.metabolite',
        #    'term': row[1],
        #})

    # print(component_ids)

    c.execute('''SELECT id, ome_id, synonym, type, data_source_id FROM synonym''')

    all_rows = c.fetchall()
    for row in all_rows:
        synonym_type = row[3]
        if synonym_type in ["reaction", "component", "compartment"]:
            data_source = data_sources[row[4]]
            collection = data_source["bigg_id"]
            term = row[2]

            # create target annotation
            Annotation.post(data_dict={
                'collection': collection,
                'term': term
            })

            # create mapping


        # print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))


    db.close()
    return reaction_ids, compartment_ids, component_ids


if __name__ == "__main__":
    #post_identifiers_collections()
    post_bigg_evidence()
    # bigg_mappings()
