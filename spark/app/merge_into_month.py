import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession

##########################
# You can configure master here if you do not pass the spark.master paramenter in conf
##########################
#master = "spark://spark:7077"
#conf = SparkConf().setAppName("Spark Hello World").setMaster(master)
#sc = SparkContext(conf=conf)
#spark = SparkSession.builder.config(conf=conf).getOrCreate()

# Create spark context
sc = SparkContext()

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

def merge_into_month(execution_date):
    for i in range(0, number_of_days_in_month(execution_date.year, execution_date.month)):
        print(i)

merge_into_month(execution_date)