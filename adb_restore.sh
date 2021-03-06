#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# AnnotateDB restore database dump
# -----------------------------------------------------------------------------
# usage:
#	./adb_restore.sh
# -----------------------------------------------------------------------------

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: "${ADB_DOCKER_COMPOSE_YAML:?The ADB environment variable must be exported: set -a && source .env.local}"

BACKUP_DIR=$DIR/releases
DB_DUMP=${BACKUP_DIR}/adb-v${ADB_VERSION}.dump

echo "-------------------------------"
echo "Restore postgres dump          "
echo "-------------------------------"

echo "Restore" $DB_DUMP

docker exec adb_postgres mkdir /backups
docker cp ${DB_DUMP} adb_postgres:/backups/
docker exec -u $ADB_DB_USER adb_postgres pg_restore -d ${ADB_DB_NAME} -v -c -U ${ADB_DB_USER} /backups/adb-v${ADB_VERSION}.dump

echo "-------------------------------"
echo "Create materialized views      "
echo "-------------------------------"
docker exec -u $ADB_DB_USER adb_postgres pg_restore -d ${ADB_DB_NAME} -v -c -U ${ADB_DB_USER} /backups/adb-v${ADB_VERSION}.dump



