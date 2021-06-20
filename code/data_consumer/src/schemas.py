from pyspark.sql.types import LongType, StructType,StructField, StringType, IntegerType, ArrayType, TimestampType, DateType

order = StructType([
    StructField("event",StringType(),True),
    StructField("messageid",StringType(),True),
    StructField("userid",StringType(),True),
    StructField("lineitems", ArrayType(StructType([
      StructField("productid",StringType(),True),
      StructField("quantity", LongType(), True)
    ])), True),
    StructField("orderid", IntegerType(), True),
    StructField("timestamp", StringType(), True)
])

product = StructType([
    StructField("event",StringType(),True),
    StructField("messageid",StringType(),True),
    StructField("userid",StringType(),True),
    StructField("properties", StructType([
        StructField("productid", StringType(), True)
    ]), True),
    StructField("context", StructType([
        StructField("source", StringType(), True)
    ]), True),
    StructField("timestamp", StringType(), True)
  ])


schemas = {
    'order': order,
    'product': product
}