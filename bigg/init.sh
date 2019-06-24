#!/usr/bin/env bash
#cd /src/git/bigg_models/bin && source ./check_running
#cd /src/git/cobradb && py.test -v .
RESULT1=$?

echo Running MNT scripts:

echo     \# Making indices
psql -h db -p 5432 -d bigg -U zaking -f /src/git/bigg_models/bigg_models/setup.sql
		
echo Restoring DB:
pg_restore -c -h db -p 5432 -d bigg -U zaking /src/database.dump

echo SERVING YOLOSWAGZ RIGHT NOW

cd /src/git/bigg_models && python -m bigg_models.server --port=8910 --processes=${PROCESSES}
