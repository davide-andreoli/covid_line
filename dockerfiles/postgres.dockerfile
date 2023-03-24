FROM postgres

COPY ../docker_entrypoints/db/*.sql /docker-entrypoint-initdb.d/


