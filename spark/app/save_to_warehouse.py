import sys
import os
from datetime import datetime
from calendar import monthrange
from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

home_dir = os.path.expanduser('~')
print(os.listdir(home_dir + '/spark'))

execution_date = datetime.strptime(os.environ.get("AIRFLOW_CTX_EXECUTION_DATE").split('T')[0], '%Y-%m-%d')

spark = SparkSession \
    .builder \
    .appName("save_to_warehouse") \
    .config("spark.sql.warehouse.dir", "/user/hive/warehouse") \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()
    # TO DO: configure DB covid_data

df = spark.read \
    .parquet(f"/usr/share/covid_data/pq/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/{execution_date.strftime('%d')}/cases_{execution_date.strftime('%Y%m%d')}.parquet")



if spark.catalog.tableExists("cases"):
    current_table = spark.read.table("cases")
    # Renoves matching rows from current table
    current_table = current_table.join(df, current_table.collection_id == df.collection_id, "leftanti")
    # Adds them back from the updated source
    current_table = current_table.union(df)
    # Save the table in hive
    current_table.write.mode("overwrite").saveAsTable("cases_temp_table")
    new_table = spark.read.table("cases_temp_table")
    # TO-DO: Change the processing logic to avoid rewriting the whole table --> delete and then append
    new_table.write \
        .mode("overwrite") \
        .insertInto("cases")
    spark.sql("DROP TABLE cases_temp_table")
else:
    #spark.sql("CREATE DATABASE IF NOT EXISTS covid_data")
    df.write \
        .partitionBy("collection_date", "country_cod") \
        .mode("overwrite") \
        .saveAsTable("cases")



# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

  # docker-compose exec hive-server bash
  # /opt/hive/bin/beeline -u jdbc:hive2://localhost:10000
