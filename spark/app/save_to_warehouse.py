import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F



spark = SparkSession \
    .builder \
    .appName("save_to_warehouse") \
    .config("spark.jars", "~/spark/postgresql-42.5.4.jar") \
    .getOrCreate()

DB_URL = "jdbc:postgresql://warehouse-db:5432/airflow"
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'


df = spark.read \
    .format("jdbc") \
    .option("url", DB_URL) \
    .option("dbtable", "movies") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .option("driver", "org.postgresql.Driver") \
    .load()

df.printSchema()

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

