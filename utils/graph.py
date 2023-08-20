from diagrams import Diagram
from diagrams.onprem.vcs import Github
from diagrams.generic.storage import Storage
from diagrams.onprem.analytics import Spark, Hive, Superset, Hadoop

graph_attr = {
    "label": ""
}

with Diagram("Pipeline", show=False, graph_attr=graph_attr):
    Github("Protezione Civile") >> Storage("Local CSV") >> Spark("Merge data") >> Hadoop("Parquet on HDFS") >> Spark("Save to warehouse") >> Hive("Data warehouse") >> Superset("Data visualization")

