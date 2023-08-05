import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

home_dir = os.path.expanduser('~')
print(os.listdir(home_dir + '/spark'))

spark_jars_packages = "org.postgresql:postgresql:42.5.1"

spark = SparkSession \
    .builder \
    .appName("save_to_warehouse") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

    #.config("spark.jars", home_dir + '/spark' + "/postgresql-42.5.4.jar") \
    #    .config("spark.sql.warehouse.dir", "/hive/warehouse/dir")

DB_URL_2 = "jdbc:hive2://hive-server:10000"
DB_USER_2 = 'hive'
DB_PASSWORD_2 = 'hive'

df = spark.read.table("pokes")

df.printSchema()

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

