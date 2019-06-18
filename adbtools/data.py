"""
Example data to test the database
"""

COLLECTIONS = [
  {
    "namespace": "sbo",
    "miriam": "true",
    "name": "Systems Biology Ontology",
    "idpattern": "SBO:\\d+",
    "urlpattern": "https://identifiers.org/sbo/{id}"
  },
  {
    "namespace": "chebi",
    "miriam": "true",
    "name": "CHEBI",
    "idpattern": "CHEBI:\\d+",
    "urlpattern": "https://identifiers.org/chebi/{id}"
  }
]

EVIDENCES = [
  {
    "source": "bigg",
    "version": "1.4",
    "evidence": "database"
  },
  {
    "source": "bigg",
    "version": "1.4",
    "evidence": "database"
  }
]


ANNOTATIONS = [
  {
    "term": "SBO:000023",
    "collection": "sbo"
  },
  {
    "term": "SBO:000024",
    "collection": "sbo"
  }
]
