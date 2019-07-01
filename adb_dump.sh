#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# PK-DB backup
# -----------------------------------------------------------------------------
# TODO: check that backup can be restored (restore script)
# usage:
#	./adb_dump.sh
# -----------------------------------------------------------------------------


DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
: "${ADB_DOCKER_COMPOSE_YAML:?The ADB environment variable must be exported: set -a && source .env.local}"

BACKUP_DIR=$DIR
VERSION=0.1
DB_DUMP=${BACKUP_DIR}/adb-v${VERSION}.dump

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
docker exec -u $ADB_DB_USER annotatedb_adb_1 pg_dump -Fc $ADB_DB_NAME > $DB_DUMP
if [ -e $DB_DUMP ]
then
    echo "SUCCESS $DB_DUMP"
else
    echo "! FAILURE $DB_DUMP !"
fi