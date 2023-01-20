FROM apache/airflow:2.5.0

ENV AIRFLOW_HOME=/opt/airflow

USER root
RUN apt-get update -qq && apt-get install vim wget default-jre -qqq

USER $AIRFLOW_UID

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

