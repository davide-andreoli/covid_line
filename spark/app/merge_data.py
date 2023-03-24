import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


spark = SparkSession.builder.appName("merge_data").getOrCreate()

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(f"/usr/share/covid_data/raw/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/cases_{execution_date.strftime('%Y%m%d')}.csv")

# All the columns should be renamed here
df = df.withColumn("data",F.to_date(F.col("data"))) 

df.write.mode('overwrite').partitionBy("data").parquet(f"/usr/share/covid_data/pq/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/cases_{execution_date.strftime('%Y%m%d')}.parquet")



