from flask import jsonify
from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, asc, col, sum
import os, json

# PRODUCTION = True if ("PRODUCTION" in os.environ) else False
#
# DATABASE_IP = os.environ["DATABASE_IP"] if ("DATABASE_IP" in os.environ) else "localhost"
# builder = SparkSession.builder.appName("productStats") .config ("spark.driver.extraClassPath", "mysql-connector-j-8.0.33.jar")
#
# if ( not PRODUCTION ):
#     builder = builder.master ( "local[*]" )\
#                     .config (
#                         "spark.driver.extraClassPath",
#                         "mysql-connector-j-8.0.33.jar"
#                     )
# spark = builder.getOrCreate()
#
# spark.sparkContext.setLogLevel(logLevel="ERROR")

PRODUCTION = True if ("PRODUCTION" in os.environ) else False
DATABASE_IP = os.environ["DATABASE_URL"] #if ("DATABASE_IP" in os.environ) else "localhost"

builder = SparkSession.builder.appName("prodStats")

if (not PRODUCTION):
    builder = builder.master("local[*]")

spark = builder.config("spark.driver.extraClassPath", "mysql-connector-j-8.0.33.jar").getOrCreate()
spark.sparkContext.setLogLevel(logLevel="ERROR")


productDF = spark.read \
    .format ( "jdbc" ) \
    .option ( "driver","com.mysql.cj.jdbc.Driver" ) \
    .option ( "url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB" ) \
    .option ( "dbtable", "shopDB.product" ) \
    .option ( "user", "root" ) \
    .option ( "password", "root" ) \
    .load ( )

# categoryDF = spark.read \
#     .format ( "jdbc" ) \
#     .option ( "driver","com.mysql.cj.jdbc.Driver" ) \
#     .option ( "url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB" ) \
#     .option ( "dbtable", "shopDB.category" ) \
#     .option ( "user", "root" ) \
#     .option ( "password", "root" ) \
#     .load ( )

orderDF = spark.read \
    .format ( "jdbc" ) \
    .option ( "driver","com.mysql.cj.jdbc.Driver" ) \
    .option ( "url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB" ) \
    .option ( "dbtable", "shopDB.order" ) \
    .option ( "user", "root" ) \
    .option ( "password", "root" ) \
    .load ( )

orderProductsDF = spark.read \
    .format ( "jdbc" ) \
    .option ( "driver","com.mysql.cj.jdbc.Driver" ) \
    .option ( "url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB" ) \
    .option ( "dbtable", "shopDB.orderproducts" ) \
    .option ( "user", "root" ) \
    .option ( "password", "root" ) \
    .load ( )


neededOrdersDF= productDF.alias("pr").join(
    orderProductsDF.alias("op"), col("op.productId")==col("pr.id")
).join(
    orderDF.alias("o"), col("o.id")==col("op.orderId")
)
print("needed orders")
print(neededOrdersDF)

totalOrders=neededOrdersDF.count()

sold=neededOrdersDF.filter(neededOrdersDF["status"]=="COMPLETE").count()

products=productDF.collect()
print(products)

statsList = []
for product in products:
    orders = neededOrdersDF.filter(neededOrdersDF["productId"]==product.id)
    # totalOrders = orders.count()
    print(f"orders for product{product.id}")
    print(orders)
    sold = orders.filter(orders["status"]=="COMPLETE").agg(sum(orders["quantity"])).collect()[0][0]
    print(sold)
    waiting = orders.filter(orders["status"]!="COMPLETE").agg(sum(orders["quantity"])).collect()[0][0]
    # waiting += orders.filter(orders["status"]=="CREATED").agg(sum(orders["quantity"])).collect()[0][0]
    # for order in orders:
    #     if order.status == "COMPLETE":
    #         sold += 1
    if sold is None:
        sold=0
    if waiting is None:
        waiting=0
    tmpStat = {
        'name': product.name,
        'sold': sold,
        'waiting': waiting
    }
    if (sold>0 or waiting>0):
        statsList.append(tmpStat)

json_result = {
    "statistics": statsList
}

# Convert the JSON structure to a JSON string
json_string = json.dumps(json_result, indent=4)
# print(result)
# print(json_result)

print(json_string)


with open("/app/prodStat.json", "w+") as f:
    f.write(json_string)

spark.stop()


