from calendar import monthrange
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

# .master("spark://spark:7077") ? --> find a way to connect to Spark cluster

def number_of_days_in_month(year, month):
    return monthrange(year, month)[1]

def merge_into_month(execution_date):
    for i in range(0, number_of_days_in_month(execution_date.year, execution_date.month)):
        print(i)