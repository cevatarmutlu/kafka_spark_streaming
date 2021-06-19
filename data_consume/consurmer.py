from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from src.schemas import schemas
from src.trasforms import transforms
import argparse
import src.config as config

def postgres_sink(data_frame, table):
    data_frame.show()
    postgres_cfg = config.get("postgres")

    url = f"jdbc:postgresql://{postgres_cfg['host']}:{postgres_cfg['port']}/{postgres_cfg['database']}"

    data_frame.write.format(postgres_cfg['format']) \
        .option("url", url) \
        .option("dbtable", table) \
        .option("user", postgres_cfg['user']) \
        .option("password", postgres_cfg['password']) \
        .option("driver", postgres_cfg['driver']) \
        .mode('append') \
        .save()

def foreach_batch_function(df, epoch_id, table):
  postgres_sink(df, table)

def getVariables():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topic', help="Topic name to read from Kafka")
    parser.add_argument('-tw', '--table', help="Table Name to write PostgreSQL")

    args = parser.parse_args()

    topic = args.topic
    table = args.table
    return topic, table

# run: spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --driver-class-path /home/sade/.local/share/DBeaverData/drivers/maven/maven-central/org.postgresql/postgresql-42.2.5.jar consumerOrderSpark.py 
if __name__ == "__main__":
    topic, table = getVariables()
    kafka_cfg = config.get("kafka")

    schema = schemas[topic]

    spark = SparkSession \
        .builder \
        .getOrCreate()

    spark.sparkContext.setLogLevel("DEBUG")

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_cfg['url']) \
        .option("subscribe", topic) \
        .option("startingOffsets", "latest") \
        .load()

    data = df.select(
        from_json(col("value").cast("string"), schema).alias("value")
    )

    # # Transfrom
    cleaning_data = transforms[topic](data)

    cleaning_data.printSchema()

    # Load
    writeStream = cleaning_data.writeStream \
        .outputMode("append") \
        .foreachBatch(lambda df, epoch_id: foreach_batch_function(df, epoch_id, table)) \
        .option("truncate", "false")\
        .start()

    writeStream.awaitTermination()