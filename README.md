<h1><img alt="AnnotateDB logo" src="./images/annotatedb_logo.png" height="100" /> AnnotateDB: database for annotation of computational models</h1>


AnnotateDB (spoken annotated bee) is a database for annotation of computational models in biology.
It's mission is to provide mapped annotation resources which simplify annotation of computational models and mapping of entities.


## Installation

To setup the development server for local development (backend & frontend):
```bash
# clone or pull the latest code
git clone https://github.com/matthiaskoenig/annotatedb.git
cd annotatedb
git pull

# set environment variables
set -a && source .env.local
 
# create/rebuild all docker containers
./docker-purge.sh
```

Development server is available accesible from
```
http://localhost:9000/
```


## Data sources
### Bigg 
https://github.com/psalvy/bigg-docker
```
git clone https://github.com/psalvy/bigg-docker.git
```
# get a database dump
https://github.com/SBRG/bigg_models_data/releases


### Miriam collections (database collections)
- created with sbmlutils


## TODO
- python package for installation
- create database interaction layer (sqlalquemy? django?)
- store data collections in database
- upload bigg synonms mapping into database
- provide example code for identifier mapping
    - query bigg synonyms (gene, metabolite, reaction)
    - query based on general annotation
- create schema documentation and make a release

---
&copy; Matthias König.