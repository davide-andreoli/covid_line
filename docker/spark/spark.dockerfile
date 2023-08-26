FROM apache/spark-py:v3.1.3

USER root
RUN pip3 install requests