"""
Could be helpful to define a database view
http://www.postgresqltutorial.com/managing-postgresql-views/
"""
import psycopg2
from collections import OrderedDict
from pprint import pprint

try:
    connection = psycopg2.connect(
        user="adb",
        password="adb",
        host="localhost",
        port="5434",
        database="adb"
    )
    cursor = connection.cursor()

    # get all the mappings
    select_query = "select * from adb_mapping"

    cursor.execute(select_query)
    mapping_records = cursor.fetchall()

    print("-" * 80)
    print("Mappings in AnnotateDB")
    print("-" * 80)
    for k, row in enumerate(mapping_records):
        entry = OrderedDict([
            ('id', row[0]),
            ('qualifier', row[1]),
            ('evidence_id', row[2]),
            ('source_id', row[3]),
            ('target_id', row[4]),
        ])
        pprint(entry)
        if k == 10:
            break
    print('...')
    print("-" * 80)

except (Exception, psycopg2.Error) as error:
    print("Error while fetching data from PostgreSQL", error)

finally:
    # closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
