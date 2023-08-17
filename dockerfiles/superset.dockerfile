FROM apache/superset:2.1.0

USER root

RUN pip install pyhive

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY ../docker_entrypoints/scripts/*.sh /superset-init.sh
RUN chmod +x /superset-init.sh

COPY docker_entrypoints/scripts/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]

# hive://hive@{hostname}:{port}/default