"""
Could be helpful to define a database view
http://www.postgresqltutorial.com/managing-postgresql-views/
"""
import sys
import logging
import psycopg2
from collections import OrderedDict
from pprint import pprint


def execute_query(query, description=None, fields=None):
    """ Executes the given query within database context.

        :param query_function:
        :return:
        """
    try:
        connection = psycopg2.connect(
            user="adb",
            password="adb",
            host="localhost",
            port="5434",
            database="adb"
        )
        cursor = connection.cursor()

        print("-" * 80)
        print(query)
        print(description)
        print("-" * 80)
        cursor.execute(query)
        mapping_records = cursor.fetchall()

        for k, row in enumerate(mapping_records):
            print(row)

            if fields is not None:
                # create dict for access
                entry = OrderedDict(zip(fields, row))
                pprint(entry)

    except (Exception, psycopg2.Error) as error:
        logging.error(f"Error while fetching data from PostgreSQL: {error}")

    finally:
        # close database connection
        if connection:
            cursor.close()
            connection.close()


def example_mappings_table():
    """ Query the adb_mapping table.

    This is the internal table for mappings (with foreign keys).
    Much simpler to query on the mapping_view instead (see next example).
    :return:
    """
    execute_query(
        query="""
        SELECT * FROM adb_mapping LIMIT 10
        """,
        description="select first 10 mappings",
        fields=['id', 'qualifier', 'evidence_id', 'source_id', 'target_id']
    )


def example_mappings_view():
    """ Using the mapping view to query mappings.

    :param cursor:
    :return:
    """
    execute_query(
        query="""
        SELECT * FROM mapping_view LIMIT 10
        """,
        description="Select first 10 mappings in dedicated mapping_view",
        fields=['id', 'source_collection', 'source_miriam', 'source_term',
                 'qualifier',
                 'target_collection', 'target_miriam', 'target_term',
                 "evidence_source", "evidence_version", "evidence"
                 ]
    )

def example_collections():
    execute_query(
        query="""
        SELECT * FROM adb_collection LIMIT 10
        """,
        description="Select first 10 collection.",
        fields=['id', 'namespace', 'miriam', 'name', 'idpattern', 'urlpattern']
    )



QUERIES = [
        [
            """
            SELECT * FROM mapping_view 
                WHERE (source_term = 'ACKr')
                ORDER BY target_namespace, target_term;
            """,
            "Query all mappings for 'ACKr'."
        ],
        [
            """
            SELECT * FROM mapping_view 
                WHERE (source_term = 'ACKr' AND 
                       source_namespace = 'bigg.reaction' AND
                       qualifier = 'IS' AND
                       target_miriam = TRUE)
                ORDER BY target_namespace, target_term;
            """,
            "Query all MIRIAM mappings for the bigg.reaction 'ACKr'"
        ],
        [
            """
            SELECT source_term FROM mapping_view 
                WHERE (target_term = 'CHEBI:698' AND
                       target_namespace = 'chebi' AND 
                       source_namespace = 'bigg.metabolite' AND
                       qualifier = 'IS')
                ORDER BY target_namespace, target_term;
            """,
            "Query bigg metabolite for the CHEBI id 'CHEBI:698'"
        ],
        [
            """
            SELECT source_term FROM mapping_view 
                WHERE (target_term = 'CHEBI:17634' AND
                       target_namespace = 'chebi' AND 
                       source_namespace = 'bigg.metabolite' AND
                       qualifier = 'IS' AND
                       evidence_source = 'bigg' AND evidence_version = '1.5' and evidence = 'database'
                       )
                ORDER BY target_namespace, target_term;
            """,
            "Restrict information to bigg evidence, multiple bigg metabolites for chebi.'"
        ]
    ]


if __name__ == "__main__":
    old_stdout = sys.stdout
    log_file = open("example_postgres.log", "w")
    sys.stdout = log_file

    # examples with creating hashmaps
    example_mappings_table()
    example_mappings_view()
    example_collections()

    # execute additional set of queries and show results
    for data in QUERIES:
        execute_query(query=data[0], description=data[1])

    sys.stdout = old_stdout
    log_file.close()