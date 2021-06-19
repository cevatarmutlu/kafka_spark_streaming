from confluent_kafka import Consumer
import pandas
import json
from datetime import datetime, timedelta
import sys
import time
import os

category = pandas.read_csv("dataprocessing/data/product-category-map.csv")

kafka_advanced_listener = 'PLAINTEXT://localhost:9092'
topic_name = 'product'

c = Consumer(
    {
    'bootstrap.servers': kafka_advanced_listener,
    'group.id': 'realtimeanalize',
    'auto.offset.reset': 'earliest'
    }
)

c.subscribe([topic_name])

timestamps = []
active_users = []
platforms = []
categories = []

while True:

    minute_ago = datetime.now() - timedelta(seconds=20)
    
    msg = c.poll(1.0)
    
    if msg == None:
        continue
    if msg.error():
        print(f"Consumer error: {msg.error()}")
        continue

    data = json.loads(msg.value())

    timestamp = datetime.strptime(data['timestamp'], '%m-%d-%Y %H:%M:%S.%f')

    # Bazen kullanıcı görüntülenme süresi belirlenen dakikadan önce çıkabiiyor. Onu önlemek için
    if timestamp > minute_ago:
        timestamps.append(timestamp)
        active_users.append(data['userid'].split("-")[1])
        platforms.append(data['context']['source'])

        df = category.query(f"productid == '{data['properties']['productid']}'")
        categoryid = df['categoryid'].values[0].split('-')[1]
        categories.append(categoryid)

    # En eklenmiş değere bakıyorum

    if len(timestamps) > 0:
            
        if timestamps[0] < minute_ago:
            timestamps.pop(0)
            active_users.pop(0)
            platforms.pop(0)
            categories.pop(0)
    
        # print(active_users)
        # print(platforms)
        # print(categories)

        data_dict = {
            'user': active_users,
            'category': categories,
            'platform': platforms
        }

        result_df = pandas.DataFrame(data=data_dict)

        print("\n\n", result_df, "\n\n")
        

c.close() # Buraya hiç girmiyor.