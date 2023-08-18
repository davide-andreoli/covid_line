FROM apache/superset:2.1.0

USER root

RUN pip install pyhive bs4

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY docker_entrypoints/superset/*.sh /superset-init.sh
RUN chmod +x /superset-init.sh

COPY docker_entrypoints/superset/superset_custom_init.py /superset_custom_init.py
RUN chmod +x /superset_custom_init.py

COPY docker_entrypoints/superset/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]

# hive://hive@hive-server:10000/default