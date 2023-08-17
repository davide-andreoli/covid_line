FROM apache/superset:latest

USER root

RUN pip install mysqlclient

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY docker_entrypoints/scripts/superset_init.sh /superset-init.sh

COPY docker_entrypoints/scripts/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]