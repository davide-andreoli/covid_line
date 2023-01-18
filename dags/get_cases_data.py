import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

URL_PREFIX = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-andamento-nazionale/' 
URL_TEMPLATE = URL_PREFIX + '/dpc-covid19-ita-andamento-nazionale-{{ execution_date.strftime(\'%Y%m%d\') }}.csv'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y%m%d\') }}.csv'

with DAG(
    dag_id="get_cases_data",
    start_date=datetime(2023,1,1),
    end_date=datetime(2023,1,10),
    schedule_interval="@daily") as dag:

    start_task = DummyOperator(task_id='start')

    wget_task = BashOperator(
        task_id='wget',
        bash_command=f'echo {OUTPUT_FILE_TEMPLATE}'
    )

    end_task = DummyOperator(task_id='end')

    start_task >> wget_task >> end_task