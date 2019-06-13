[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1406979.svg)](https://doi.org/10.5281/zenodo.1406979)
[![GitHub version](https://badge.fury.io/gh/matthiaskoenig%2Fannotatedb.svg)](https://badge.fury.io/gh/matthiaskoenig%2Fannotatedb)

<h1><img alt="AnnotateDB logo" src="./images/annotatedb_logo.png" height="100" /> AnnotateDB</h1>
<b><a href="https://orcid.org/0000-0003-1725-179X" title="https://orcid.org/0000-0003-1725-179X"><img src="./docs/images/orcid.png" height="15" width="15"/></a> Matthias König</b>
and
<b><a href="https://orcid.org/0000-0002-4588-4925" title="0000-0002-4588-4925"><img src="./docs/images/orcid.png" height="15"/></a> Jan Grzegorzewski</b>


`AnnotateDB` (pronounced `annotated bee`) is a database for mapping of annotations found in computational models in biology.
It's mission is to provide mapped annotation resources which simplify annotation of computational models and mapping of entities in such models.

A major source of information is the (http://bigg.ucsd.edu/)(BiGG Database).

The database consists of the following main tables:
- `collection`: A data source or miriam collection for annotation or xref information
- `annotation`: The combination of a term from a collection and the given collection
- `mapping`: Mapping between annotations, from source annotation to target annotation. The kind of mapping is defined by the qualifier. E.g. the qualifier `BQM_IS` encodes that the source annotation `is` the target annotation.
- `evidence`: Evidence for the given mapping between annotations.

<img alt="Database schema" src="./images/schema_v0.0.1.png" width="400"/>

## Data sources

### Bigg
Bigg models are included based on database dump from:
https://github.com/SBRG/bigg_models_data/releases 


### Miriam collections (database collections)
Information on the collections is based on identifiers.org collection retrieved 
with `sbmlutils`.

## Installation
### Setup the development server
AnnotateDB is distributed as `docker` containers and `docker-compose` files. 

To setup the development server for local development (backend & frontend):
```bash
# clone or pull the latest source code
git clone https://github.com/matthiaskoenig/annotatedb.git
cd annotatedb

# set environment variables
set -a && source .env.local
 
# create/rebuild all docker containers
./docker-purge.sh
```
The django development server is accessible via
```
http://localhost:9000/
```

### Setup the database
Information to come.

---
&copy; Matthias König and Jan Grzegorzewski