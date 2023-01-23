import os
from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

with DAG(
    dag_id="test_spark",
    start_date=datetime(2022,12,20),
    end_date=datetime(2023,1,10),
    schedule_interval="@daily") as dag:

    start_task = DummyOperator(task_id='start')

    merge_into_month_task = SparkSubmitOperator(
        task_id="merge_into_month_task",
        application="/usr/local/spark/app/merge_into_month.py",
        name="merge_into_month",
        conn_id="spark_default", # Should be configured to use spark_master
        verbose=1,
        conf={"spark.master":"spark://spark:7077"},
        application_args=[],
        dag=dag
    )

    end_task = DummyOperator(task_id='end')

    start_task >> merge_into_month_task >> end_task

