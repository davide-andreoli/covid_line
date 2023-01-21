import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/' 
URL_TEMPLATE = URL_PREFIX + '/dpc-covid19-ita-andamento-nazionale-{{ execution_date.strftime(\'%Y%m%d\') }}.csv'
OUTPUT_FILE_TEMPLATE = 'raw_cases_{{ execution_date.strftime(\'%Y%m%d\') }}.csv'

with DAG(
    dag_id="get_cases_data",
    start_date=datetime(2022,12,20),
    end_date=datetime(2023,1,10),
    schedule_interval="@daily") as dag:

    start_task = DummyOperator(task_id='start')

    download_data_task = BashOperator(
        task_id='download_data',
        bash_command=f'curl -sSL -o {OUTPUT_FILE_TEMPLATE} {URL_TEMPLATE}'
    )

    merge_into_month_task = SparkSubmitOperator(
        task_id="merge_into_month_task",
        application="/usr/local/spark/app/merge_into_month.py",
        name="merge_into_month",
        conn_id="spark_local",
        verbose=1,
        conf={"spark.master":"spark://spark:7077"},
        application_args=[],
        dag=dag
    )

    end_task = DummyOperator(task_id='end')

    start_task >> download_data_task >> merge_into_month_task >> end_task

