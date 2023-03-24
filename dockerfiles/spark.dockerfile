FROM docker.io/bitnami/spark:3.3

USER root
RUN apt-get update -qq && apt-get install vim curl wget default-jre -qqq

USER $AIRFLOW_UID

RUN curl https://jdbc.postgresql.org/download/postgresql-42.5.4.jar --create-dirs -o ~/spark/postgresql-42.5.4.jar


COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

