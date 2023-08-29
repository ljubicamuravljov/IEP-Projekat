from flask import Flask, json, jsonify
from flask import request

application = Flask ( __name__ )

import os
import subprocess
# @application.route ( "/simple" )
# def simple ( ):
#     os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/simple.py"
#     result = subprocess.check_output ( ["/template.sh"] )
#     return result.decode ( )

# @application.route("/database")
# def database():
#     os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/database.py"
#
#     os.environ[
#         "SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"
#
#     result = subprocess.check_output(["/template.sh"])
#     return result.decode()

@application.route("/catStat", methods=["GET"])
def category_statistics():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/categoryStats.py"
    os.environ["SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"

    result = subprocess.run(["/template.sh"])

    rez = []

    file = open("app/catStat.json", "r")

    rez = json.load(file)
    print(rez)
    # rez.append(data)  # dodas jedan po jedan red a red je json obj sta si procitala od statistika

    file.close()

    return rez, 200

@application.route("/prodStat", methods=["GET"])
def product_statistics():
    os.environ["SPARK_APPLICATION_PYTHON_LOCATION"] = "/app/productStats.py"
    os.environ["SPARK_SUBMIT_ARGS"] = "--driver-class-path /app/mysql-connector-j-8.0.33.jar --jars /app/mysql-connector-j-8.0.33.jar"

    result = subprocess.run(["/template.sh"])

    rez = []

    file= open("app/prodStat.json","r")
    # for row in file:
    rez=json.load(file)
        # print(data)
        # rez.append(data) # dodas jedan po jedan red a red je json obj sta si procitala od statistika

    file.close()

    return rez, 200

if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0", port=5004)
