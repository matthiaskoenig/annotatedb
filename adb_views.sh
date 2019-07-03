#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Execute SQL to create materialized views
# -----------------------------------------------------------------------------
# usage:
#	./adb_views.sh
# -----------------------------------------------------------------------------

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: "${ADB_DOCKER_COMPOSE_YAML:?The ADB environment variable must be exported: set -a && source .env.local}"


echo "-------------------------------"
echo "Create materialized views      "
echo "-------------------------------"
docker exec annotatedb_adb_1 mkdir /sql
docker cp ${DIR}/adb/create_views.sql annotatedb_adb_1:/sql/
docker exec -u $ADB_DB_USER annotatedb_adb_1 psql -d ${ADB_DB_NAME} -v -U ${ADB_DB_USER} -a -f /sql/create_views.sql



