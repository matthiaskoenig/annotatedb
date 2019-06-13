<h1><img alt="AnnotateDB logo" src="./images/annotatedb_logo.png" height="100" /> AnnotateDB: database for annotation of computational models</h1>


AnnotateDB (spoken annotated bee) is a database for annotation of computational models in biology.
It's mission is to provide mapped annotation resources which simplify annotation of computational models and mapping of entities.


## Installation

### virtualenv
Create virtual environment with `virtualenv` & `virtualenvwrapper`.
```
mkvirtualenv annotatedb --python=python3.6
```
If this is not working use
```
which python3.6
```
to find the path to python and use it in the command above.

```
git clone https://github.com/matthiaskoenig/annotatedb.git
cd annotatedb
workon annotatedb
(annotatedb) pip install -e . --upgrade

# Install jupyter kernel (for notebook execution)
(annotatedb) pip install jupyterlab --upgrade
(annotatedb) python -m ipykernel install --user --name=pancreas
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