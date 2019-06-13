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


import json


# -----------------------------------------------------------------------------
# identifiers.org collection
# -----------------------------------------------------------------------------
def load_miriam():
    """ Loads miriam registry file.

    :return:
    """
    f_miriam = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'resources', 'IdentifiersOrg-Registry.json'
    )

    with open(f_miriam) as fp:
        d = json.load(fp)

    return d


MIRIAM_COLLECTION = load_miriam()