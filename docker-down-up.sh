#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Brings all containers down and up again
# -----------------------------------------------------------------------------

: "${ADB_DOCKER_COMPOSE_YAML:?The 'PKDB_*' environment variables must be exported.}"
docker-compose -f $ADB_DOCKER_COMPOSE_YAML down && docker-compose -f $ADB_DOCKER_COMPOSE_YAML up --detach