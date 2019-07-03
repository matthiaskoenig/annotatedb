#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Brings all containers down and up again


# To rebuild a singe container use
# docker-compose -f $ADB_DOCKER_COMPOSE_YAML up -d --no-deps --build <service_name>
# -----------------------------------------------------------------------------

: "${ADB_DOCKER_COMPOSE_YAML:?The 'ADB_*' environment variables must be exported.}"
docker-compose -f $ADB_DOCKER_COMPOSE_YAML down --remove-orphans && docker-compose -f $ADB_DOCKER_COMPOSE_YAML up --detach