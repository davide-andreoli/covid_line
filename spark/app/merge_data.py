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

# TO-DO: rename date to something else to free up reserved name, same for id
# Column renaming
df = df.withColumnRenamed("data", "date")
df = df.withColumnRenamed("nuovi_positivi", "new_positive_cases")
df = df.withColumnRenamed("stato", "country_cod")

# Data types transformation
df = df.withColumn("date",F.to_date(F.col("date"))) 

# New columns creation
df = df.withColumn("id",F.md5(F.concat(F.col("date"),F.col("country_cod"))))

# Select only relevant colums

df = df.select("id","date","country_cod","new_positive_cases")

df.write.mode('overwrite').partitionBy("country_cod").parquet(f"/usr/share/covid_data/pq/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/cases_{execution_date.strftime('%Y%m%d')}.parquet")



