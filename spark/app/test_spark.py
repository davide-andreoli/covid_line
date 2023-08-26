import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark import SparkFiles

spark = SparkSession.builder.appName("merge_data").getOrCreate()

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(f"/usr/share/covid_data/raw/full-2023-08-26.csv")

df.printSchema()


