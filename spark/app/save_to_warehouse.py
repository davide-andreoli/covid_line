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
    .config("hive.metastore.uris", "thrift://hive-metastore:9083") \
    .enableHiveSupport() \
    .getOrCreate()

    #.config("spark.jars", home_dir + '/spark' + "/postgresql-42.5.4.jar") \
    #    .config("spark.sql.warehouse.dir", "/hive/warehouse/dir")

df = spark.read \
    .parquet(f"/usr/share/covid_data/pq/{execution_date.strftime('%Y')}/{execution_date.strftime('%m')}/cases_{execution_date.strftime('%Y%m%d')}.parquet")

df.printSchema()

if spark.catalog.tableExists("cases"):
    current_table = spark.read.table("cases")
    # Renoves matching rows from current table
    current_table.join(df, current_table.id == df.id, "leftanti")
    # Adds them back from the updated source
    current_table.union(df)
    # Save the table in hive
    # TO-DO: Change the processing logic to avoid rewriting the whole table --> delete and then append
    current_table.write.mode("overwrite").saveAsTable("cases")
else:
    df.write.mode("overwrite").saveAsTable("cases")



# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

  # docker-compose exec hive-server bash
  # /opt/hive/bin/beeline -u jdbc:hive2://localhost:10000
