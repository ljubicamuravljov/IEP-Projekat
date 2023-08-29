FROM bde2020/spark-python-template:3.3.0-hadoop3.3

# ENV SPARK_APPLICATION_PYTHON_LOCATION /app/twitter.py
#ENTRYPOINT ["spark-submit", "/app/your_spark_app.py"]

COPY statistics/main.py /app/main.py
COPY statistics/mysql-connector-j-8.0.33.jar /app/mysql-connector-j-8.0.33.jar
COPY statistics/productStats.py /app/productStats.py
COPY statistics/categoryStats.py /app/categoryStats.py

CMD [ "python3", "/app/main.py" ]
