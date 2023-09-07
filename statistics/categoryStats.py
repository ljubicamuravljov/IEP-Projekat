from pyspark.sql import SparkSession
from pyspark.sql.functions import desc, asc, col, sum, count
import os, json

PRODUCTION = True if ("PRODUCTION" in os.environ) else False

DATABASE_IP = os.environ["DATABASE_URL"] if ("DATABASE_URL" in os.environ) else "localhost"
builder = SparkSession.builder.appName("catStats") .config ("spark.driver.extraClassPath", "mysql-connector-j-8.0.33.jar")

if ( not PRODUCTION ):
    builder = builder.master ( "local[*]" )\
                    .config (
                        "spark.driver.extraClassPath",
                        "mysql-connector-j-8.0.33.jar"
                    )
spark = builder.getOrCreate()

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
    .collect()
)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!SORTEDSVEKRAJ")
print(sorted_category_stats)

# Generisanje JSON objekta
json_result = {
    "statistics": [name[0] for name in sorted_category_stats]
}

json_string = json.dumps(json_result, indent=4)
print(json_result)


print(json_string)
with open("/app/catStat.json", "w+") as f:
    f.write(json_string)

spark.stop()
