FROM apache/airflow:2.5.0

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install vim wget default-jre -qqq

USER $AIRFLOW_UID

RUN wget -P /spark/ https://jdbc.postgresql.org/download/postgresql-42.5.4.jar

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

