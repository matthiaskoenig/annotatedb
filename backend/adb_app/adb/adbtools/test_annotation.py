from backend.adb_app.adb.adbtools.data import ANNOTATIONS
from backend.adb_app.adb.adbtools.orm import OrmAnnotation

if __name__ == "__main__":

    for annotation in ANNOTATIONS:
        OrmAnnotation.post(data_dict=annotation)
