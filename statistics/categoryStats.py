from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, asc, col, sum, count
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
DATABASE_IP = os.environ["DATABASE_URL"]  # if ("DATABASE_IP" in os.environ) else "localhost"

builder = SparkSession.builder.appName("catStats")

if (not PRODUCTION):
    builder = builder.master("local[*]")

spark = builder.config("spark.driver.extraClassPath", "mysql-connector-j-8.0.33.jar").getOrCreate()
spark.sparkContext.setLogLevel(logLevel="ERROR")

productDF = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB") \
    .option("dbtable", "shopDB.product") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

categoryDF = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB") \
    .option("dbtable", "shopDB.category") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

orderDF = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB") \
    .option("dbtable", "shopDB.order") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

productCategoriesDF = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB") \
    .option("dbtable", "shopDB.productcategories") \
    .option("user", "root") \
    .option("password", "root") \
    .load()

orderProductsDF = spark.read \
    .format("jdbc") \
    .option("driver", "com.mysql.cj.jdbc.Driver") \
    .option("url", f"jdbc:mysql://{DATABASE_IP}:3306/shopDB") \
    .option("dbtable", "shopDB.orderproducts") \
    .option("user", "root") \
    .option("password", "root") \
    .load()
# Kreirajte Spark sesiju


# # # Učitajte DataFrame-ove
# # product_categories_df = spark.table("productcategories")
# # categories_df = spark.table("category")
#
# ## Treba da joinujem order sa orderproduct sa productcateory, groupby cateory i onda check complete i to
# print("ORDER DF")
# print(orderDF)
#
#
# orderProductsCompleteDF= orderProductsDF.alias("op").join(
#     orderDF.alias("o"), col("op.orderId")==col("o.id")
# ).filter(col("o.status")=="COMPLETE")
#
# # orderProductsCompleteDF=orderProductsDF.join(orderDF,orderDF["id"]==orderProductsDF["orderId"]).filter(orderDF["status"]=="COMPLETE")
# # sad imam samo komplitovane porudzbine, sad njih joinujem sa productCategories
# print ("order product completed")
# print(orderProductsCompleteDF)
#
# # tmpDF= categoryDF.alias("c").join(
# #     productCategoriesDF.alias("pc"), col("pc.categoryId")==col("c.id")
# # ).join(orderProductsCompleteDF.alias("opc"),col("pc.productId")==col("opc.productId"))
# # # tm1=categoryDF.join(productCategoriesDF,categoryDF["id"]==productCategoriesDF["categoryId"])
# # # tmpDF= tm1.join(orderProductsCompleteDF,tm1["cateoryId"]==orderProductsCompleteDF["categoryId"],"left_outer")
# #
# # #odavde spojis sa category da izvuces name
# #
# # print ("category completed")
# # print(tmpDF)
# # grupisanDf=tmpDF.groupBy("categoryId").agg(count("pc.productId").alias("product_count"))
# #
# # print("grupisani")
# # print(grupisanDf)
# #
# # sortiraniDF=grupisanDf.orderBy(desc("product_count"),asc("c.name"))
# # # Create a DataFrame with the count of delivered products per category
# # productCountDF = productCategoriesDF.groupBy("categoryId").agg(count("productId").alias("product_count"))
# #
# # # Join categories with product counts
# # categoryStatsDF = categoryDF.join(productCountDF, categoryDF["id"] == productCountDF["cateoryId"], "left_outer")
# #
# # # Sort the DataFrame by product count and name
# # sorted_category_stats_df = categoryStatsDF.orderBy(desc("product_count"), asc("name"))
# #
# # # Show the array of category names
# # result = sortiraniDF.select("c.name").collect()
# print(categoryDF)
# for row in categoryDF:
#     print(row)
#
# #OVO BRISES
# # category_info = category_df.alias("category") \
# # 	.join(product_category_df.alias("product_category"), col("category.id") == col("product_category.category_id"), "left") \
# # 	.join(product_df.alias("product"), col("product_category.product_id") == col("product.id"), "left") \
# # 	.join(order_product_df.alias("order_product"), col("product.id") == col("order_product.product_id"), "left") \
# # 	.join(order_df.alias("order1"), col("order_product.order_id") == col("order1.id"), "left") \
# # 	.groupBy("category.name") \
# # 	.agg(sum(when(col("order1.status") == "COMPLETE", col("order_product.quantity")).otherwise(lit(0))).alias("sold")) \
# # 	.orderBy(col("sold").desc(), col("category.name"))
# #
# # category_names = [str(row["name"]) for row in category_info.collect()]
#
#
#
#
#
# # Convert the list of Row objects to a list of strings
# category_names = [row.name for row in result]
#
# # Create the JSON structure
# json_result = {
#     "statistics": category_names
# }

# Kreiranje privremenog pogleda za spajanje tablica
order_products_with_categories = orderDF.alias("o").join(orderProductsDF.alias("op"),
                                                         col("o.id") == col("op.orderId")).join(
    productCategoriesDF.alias("pc"), col("op.productId") == col("pc.productId")).select("orderId", "categoryId","quantity").filter(
    col("o.status") == "COMPLETE")

# Izračunavanje broja proizvoda po kategorijama

category_product_counts = order_products_with_categories.groupby("categoryId").agg(
    sum("quantity").alias("productCount"))

# Spajanje sa imenima kategorija
category_product_counts_with_names =categoryDF.alias("c").join(category_product_counts.alias("cpc"), col("cpc.categoryId") == col("c.id"),"left_outer").fillna(0, subset=["productCount"]).select("c.name", "productCount")

# Sortiranje statistika
sorted_category_stats = (
    category_product_counts_with_names
    .orderBy(desc("productCount"), asc("c.name"))
    .select("c.name")
    # .rdd.flatMap(lambda x: x)
    .collect()
)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SORTEDSVEKRAJ")
print(sorted_category_stats)

# Generisanje JSON objekta
json_result = {
    "statistics": [name[0] for name in sorted_category_stats]
}

# Convert the JSON structure to a JSON string
json_string = json.dumps(json_result, indent=4)
print(json_result)
# print(json_result)

print(json_string)
with open("/app/catStat.json", "w+") as f:
    f.write(json_string)

spark.stop()
