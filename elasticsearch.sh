#!/usr/bin/env bash
docker exec -it adb_backend bash -c "python manage.py search_index --create -f"
docker exec -it adb_backend bash -c "python manage.py search_index --populate -f"