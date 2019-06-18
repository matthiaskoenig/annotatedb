# Build the image
#     docker image build -t bigg .
#     docker container run --rm -it --name bigg -p 5436:5432 bigg 


# Restore the dump
#     docker exec -it bigg bash
#     pg_restore -c -p 5432 -d bigg -U postgres bigg-v1.5.dump
#     psql -U postgres -d bigg


FROM postgres
COPY 001-init.sql /docker-entrypoint-initdb.d/001-init.sql

# COPY bigg-v1.5.dump /docker-entrypoint-initdb.d/010-bigg-v1.5.sql

# COPY setup.sql setup.sql
COPY bigg-v1.5.dump bigg-v1.5.dump

# CMD psql -p 5432 -d bigg -U zaking -f setup.sql
#