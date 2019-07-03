#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Complete purge of all containers and images !
#
# Execute via setting environment variables
#     set -a && source .env.local (develop)
#     ./docker-purge.sh
# -----------------------------------------------------------------------------
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: "${ADB_DOCKER_COMPOSE_YAML:?The ADB environment variable must be exported: set -a && source .env.local}"

sudo echo "Purging database and all docker containers, volumes, images ($ADB_DOCKER_COMPOSE_YAML)"

# shut down all containers (remove images and volumes)
docker-compose -f $ADB_DOCKER_COMPOSE_YAML down --volumes --rmi local

# make sure containers are removed (if not running)
docker container rm -f adb_backend
docker container rm -f adb_frontend
docker container rm -f adb_postgres
docker container rm -f adb_elasticsearch
docker container rm -f adb_nginx
docker container rm -f adb_kibana

# make sure images are removed
docker image rm -f adb_backend:latest
docker image rm -f adb_frontend:latest
docker image rm -f adb_adb:latest
docker image rm -f adb_elasticsearch:latest
docker image rm -f adb_nginx:latest

# make sure volumes are removed
docker volume rm -f annotatedb_django_media
docker volume rm -f annotatedb_django_static
docker volume rm -f annotatedb_elasticsearch_data
docker volume rm -f annotatedb_adb_data
docker volume rm -f annotatedb_vue_dist
docker volume rm -f annotatedb_node_modules

# cleanup all dangling images, containers, volumes and networks
docker system prune --force

# remove migrations
cd $DIR
sudo find . -maxdepth 5 -path "*/migrations/*.py" -not -name "__init__.py" -delete
sudo find . -maxdepth 5 -path "*/migrations/*.pyc" -delete

# remove media and static files
sudo rm -rf media
sudo rm -rf static

# build and start containers
docker-compose -f $ADB_DOCKER_COMPOSE_YAML build --no-cache

echo "*** Make migrations & collect static ***"
docker-compose -f $ADB_DOCKER_COMPOSE_YAML run --rm backend bash -c "/usr/local/bin/python manage.py makemigrations && /usr/local/bin/python manage.py migrate && /usr/local/bin/python manage.py collectstatic --noinput "

echo "*** Setup admin user ***"
docker-compose -f $ADB_DOCKER_COMPOSE_YAML run --rm backend bash -c "/usr/local/bin/python manage.py createsuperuser2 --username admin --password ${ADB_ADMIN_PASSWORD} --email koenigmx@hu-berlin.de --noinput"

# echo "*** Build elasticsearch index ***"
# docker-compose -f $ADB_DOCKER_COMPOSE_YAML run --rm backend ./manage.py search_index --rebuild -f

echo "*** Running containers ***"
docker-compose -f $ADB_DOCKER_COMPOSE_YAML up --detach
docker container ls

