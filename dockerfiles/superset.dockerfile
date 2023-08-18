FROM apache/superset:2.1.0

USER root

RUN apt-get update && apt-get install -y zip unzip
RUN pip install pyhive

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY docker_entrypoints/superset/*.sh /superset-init.sh
RUN chmod +x /superset-init.sh

COPY docker_entrypoints/superset/import_connections /superset_import_connections
RUN zip -r /import_connections.zip /superset_import_connections

COPY docker_entrypoints/superset/import_dashboards /superset_import_dashboards
RUN zip -r /import_dashboards.zip /superset_import_dashboards

COPY docker_entrypoints/superset/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]

# hive://hive@hive-server:10000/default