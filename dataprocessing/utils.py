from pyspark.sql.types import LongType, StructType,StructField, StringType, IntegerType, ArrayType, TimestampType, DateType
from pyspark.sql.functions import col, split, explode, to_timestamp, lit

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

def orderTransform(data):
    userid = split(data['value']['userid'], '-')
    products_line_by_line = data.select(
        data['value']['orderid'].alias("orderid"), 
        userid.getItem(1).alias("userid"), 
        explode(data['value']['lineitems']).alias('products_line_by_line'),
        to_timestamp(lit(data['value']['timestamp']),'MM-dd-yyyy HH:mm:ss.SSSS').alias('timestamp')
    )

    product = split(products_line_by_line['products_line_by_line']['productid'], '-')

    cleaning_data = products_line_by_line.select(
        'orderid', 
        col('userid').cast('integer'), 
        product.getItem(1).alias('productid').cast('integer'), 
        products_line_by_line['products_line_by_line']['quantity'].alias("quantity")
    )

    return cleaning_data

def productTransform(data):
    userid = split(data['value']['userid'], '-')
    productid = split(data['value']['properties']['productid'], '-')

    products_line_by_line = data.select(
        userid.getItem(1).alias("userid").cast("integer"), 
        productid.getItem(1).alias("productid").cast("integer"),
        data['value']['context']['source'].alias("source"),
        to_timestamp(lit(data['value']['timestamp']),'MM-dd-yyyy HH:mm:ss.SSSS').alias('timestamp')
    )

    return products_line_by_line


transforms = {
    'order': orderTransform,
    'product': productTransform
}
