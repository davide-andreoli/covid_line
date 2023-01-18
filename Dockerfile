FROM apache/airflow:2.5.0

ENV AIRFLOW_HOME=/opt/airflow

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER $AIRFLOW_UID