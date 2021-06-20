from pyspark.sql import SparkSession
import pyspark.sql.functions as f
import config as config


def generate_session(jar_path):
    return SparkSession \
        .builder \
        .config("spark.jars", jar_path) \
        .getOrCreate()

def read_csv(spark, filePath):
    return spark \
        .read \
        .option('header', 'true') \
        .csv(filePath)

def transfromData(data, transformFunc):
    return transformFunc(data)


# Burası özel alan. Normalde olmaması gerekir.
def transfromProCatCsv(dataFrame):
    productid = f.split(dataFrame['productid'], '-')
    categoryid = f.split(dataFrame['categoryid'], '-')

    return dataFrame.select(
        productid.getItem(1).alias("productid").cast('integer'),
        categoryid.getItem(1).alias("categoryid").cast('integer')
    )

def writeToPostgre(dataFrame, tableName):
    cfg = config.get('postgres')

    dataFrame \
        .write \
        .format(cfg['format']) \
        .option("url", f"jdbc:postgresql://{cfg['host']}:{cfg['port']}/{cfg['database']}") \
        .option("dbtable", tableName) \
        .option("user", cfg['user']) \
        .option("password", cfg['password']) \
        .option("driver", cfg['driver']) \
        .mode('append') \
        .save()


if __name__ == '__main__':
    spark_jars = '/home/sade/.local/share/DBeaverData/drivers/maven/maven-central/org.postgresql/postgresql-42.2.5.jar'
    session = generate_session(spark_jars)
    df = read_csv(session, 'data/product-category-map.csv')
    transformed_df = transfromData(df, transfromProCatCsv)
    writeToPostgre(transformed_df, 'order_product')
