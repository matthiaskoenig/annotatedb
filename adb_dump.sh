#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# AnnotateDB database dump
# -----------------------------------------------------------------------------
# usage:
#	./adb_dump.sh
# -----------------------------------------------------------------------------


DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: "${ADB_DOCKER_COMPOSE_YAML:?The ADB environment variable must be exported: set -a && source .env.local}"

BACKUP_DIR=$DIR/releases
DB_DUMP=${BACKUP_DIR}/adb-v${ADB_VERSION}.dump

if [ -e $DB_DUMP ]
then
    read -p "Overwrite existing database dump $DB_DUMP [y/N]? " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
        exit 1
    fi
fi


echo "-------------------------------"
echo "Create postgres dump"
echo "-------------------------------"
mkdir -p $BACKUP_DIR
echo "Backup to" $BACKUP_DIR
docker exec -u $ADB_DB_USER adb_postgres pg_dump -v -Fc $ADB_DB_NAME > $DB_DUMP
if [ -e $DB_DUMP ]
then
    echo "SUCCESS $DB_DUMP"
else
    echo "! FAILURE $DB_DUMP !"
fi