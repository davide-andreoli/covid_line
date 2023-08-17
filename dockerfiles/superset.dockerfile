FROM apache/superset:latest

USER root

RUN pip install pyhive

ENV ADMIN_USERNAME "superset"
ENV ADMIN_EMAIL "superset@superset.com"
ENV ADMIN_PASSWORD "superset"

COPY ../docker_entrypoints/scripts/superset-init.sh /superset-init.sh

COPY ./docker_entrypoints/scripts/superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]