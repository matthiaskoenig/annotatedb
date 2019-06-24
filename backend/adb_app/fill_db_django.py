"""
Data source table

"""
import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'adb_app.settings'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

import logging
import django
django.setup()

from adb_app.annotations.models import Collection


if __name__ == "__main__":
    collection = Collection(
        namespace="test_namespace",
        miriam=False,
        idpattern="\d+",
        urlpattern="https://test.com/{$id}"
    )
    collection.save()
