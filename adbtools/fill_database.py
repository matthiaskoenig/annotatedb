
import json
import requests

from adbtools.annotatedb import Collection, Evidence


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


def post_bigg_annotations():
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
    



if __name__ == "__main__":
    # post_identifiers_collections()
    post_bigg_annotations()
