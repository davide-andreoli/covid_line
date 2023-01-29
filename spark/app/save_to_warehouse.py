import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


spark = SparkSession.builder.appName("merge_into_month").getOrCreate()

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(f"/usr/share/covid_data/lake/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/")

df = df.withColumn("data",F.to_date(F.col("data"))) 

df.write.parquet(f"/usr/share/covid_data/lake/{execution_date.strftime('%Y')}-{execution_date.strftime('%m')}.parquet", mode='overwrite')
