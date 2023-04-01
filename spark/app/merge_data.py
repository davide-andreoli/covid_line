import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

DB_URL = "jdbc:postgresql://warehouse-db:5432/airflow"
DB_USER = 'airflow'
DB_PASSWORD = 'airflow'

spark = SparkSession.builder.appName("merge_data").getOrCreate()

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(f"/usr/share/covid_data/raw/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/cases_{execution_date.strftime('%Y%m%d')}.csv")

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

# Delete data of same day first

df.write.mode("append").format("jdbc") \
    .option("url", DB_URL) \
    .option("driver", "org.postgresql.Driver") \
    .option("dbtable", "covid_cases") \
    .option("user", DB_USER) \
    .option("password", DB_PASSWORD).save()





df.write.mode('overwrite').partitionBy("data").parquet(f"/usr/share/covid_data/pq/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/cases_{execution_date.strftime('%Y%m%d')}.parquet")



