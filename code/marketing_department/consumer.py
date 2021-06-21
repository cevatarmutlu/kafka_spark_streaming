from confluent_kafka import Consumer
import pandas
import json
from datetime import datetime, timedelta
import src.config as config

category = pandas.read_csv("src/product-category-map.csv")
kafka = config.get('kafka')


kafka_advanced_listener = kafka['url']
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
    
        data_dict = {
            'user': active_users,
            'category': categories,
            'platform': platforms
        }

        active_users_df = pandas.DataFrame(data={'userid': active_users})
        categories_df = pandas.DataFrame(data={'category': categories}).groupby('category').size()
        platforms_df = pandas.DataFrame(data={'platform': platforms}).groupby('platform').size()

        print("\n\n", datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
        print(active_users_df, "\n")
        print(categories_df, "\n")
        print(platforms_df, "\n\n")
        

c.close() # Buraya hiç girmiyor.