"""
    Bu script Kafka' ya veri yazacak olan producer' ları temsil eden script' tir.
    
    Çalıştırma örneği:
        python3 producer.py -t order -f data/orders.json -s 60

        -t -> Verinin yazılacağı topic adı
        -f -> Json dosyasının yolu
        -s -> Verilerin ne kadar sürede bir yazılacağını belirleyen değer. Saniye cinsinden

"""

from confluent_kafka import Producer
import time
import json
import argparse
from datetime import datetime

from src.ndjson import get_data
import src.config as config

def getVariables():
    """
        Bu fonksiyon bu script' e parametre olarak verilen değerleri alır.

        Return:
            (topic, file_path, second):     topic       -> Verinin yazılacağı Kafka topic' i
                                            file_path   -> ndjson dosyasının yolu
                                            second      -> Kafka' ya veri yazılma süresi. Saniye cinsinden.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--topic', help="Verinin yazılacağı Kafka topic' i")
    parser.add_argument('-f', '--file', help="ndjson dosyasının yolu")
    parser.add_argument('-s', '--second', type=int, help="Kafka' ya veri yazılma süresi. Saniye cinsinden.")

    args = parser.parse_args()

    topic = args.topic
    file_path = args.file
    second = args.second
    return topic, file_path, second

def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    # Kafka için aldığım hazır fonksiyon.
    
    if err != None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to topic: {}, partition: [{}]'.format(msg.topic(), msg.partition()))

if __name__ == "__main__":

    # product-views.json: python3 dataprocessing/producer.py -t product -f dataprocessing/data/product-views.json -s 1
    # orders.json: python3 producer.py -t order -f dataprocessing/data/orders.json -s 60

    topic, file_path, second = getVariables()

    datas = get_data(file_path)

    kafka_cfg = config.get("kafka")

    p = Producer(
        {'bootstrap.servers': kafka_cfg['url']}
    )

    for data in datas:

        now = datetime.now().strftime("%m-%d-%Y %H:%M:%S.%f")
        data['timestamp'] = str(now)[:-3]

        p.poll(0)

        p.produce(
            topic=topic,
            value=json.dumps(data),
            callback=delivery_report
        )
        p.flush()

        time.sleep(second)