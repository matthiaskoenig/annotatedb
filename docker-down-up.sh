#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Brings all containers down and up again
# docker-compose -f $ADB_DOCKER_COMPOSE_YAML up --detach --build adb
# -----------------------------------------------------------------------------

: "${ADB_DOCKER_COMPOSE_YAML:?The 'ADB_*' environment variables must be exported.}"
docker-compose -f $ADB_DOCKER_COMPOSE_YAML down --remove-orphans && docker-compose -f $ADB_DOCKER_COMPOSE_YAML up --detach