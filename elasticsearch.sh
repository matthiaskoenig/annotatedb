#!/usr/bin/env bash
docker exec -it annotatedb_backend_1 bash -c "python manage.py search_index --create -f"
docker exec -it annotatedb_backend_1 bash -c "python manage.py search_index --populate -f"