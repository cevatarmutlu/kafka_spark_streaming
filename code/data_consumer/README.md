## Data Consumer

Bu sistem `Kafka`' daki belirli `topic`' lerde bulunan veriyi `Spark streaming` okur, okuduğu veriyi temizleyerek `postgreSQL` veritabanındaki belirli tablolara yazar.

## İçindekiler

* [Nasıl Kurulur](#nasıl-kurulur)
* [Çalışma Sistemi](#calisma-sistemi)
* [Nasıl Çalıştırılır](#nasıl-çalıştırılır)
* [Eksikler ve Hatalar](#eksikler-ve-hatalar)

### Nasıl Kurulur?

Öncelikle sisteminizde `Kafka` ve `Spark` kurulu olmalıdır. `Spark` kurulumu ile ilgili bir şey anlatılmayacaktır. Bu sistem geliştirilirken `Kafka` kurulumu için `docker` kullanılmıştır. Kullanmış olduğum `docker-compose` dosyası aşağıdaki gibidir;

```yaml
version: '2'
services: 
    zookeeper:
        image: confluentinc/cp-zookeeper:latest
        environment: 
            ZOOKEEPER_CLIENT_PORT: 2181
    
    kafka:
        image: confluentinc/cp-kafka:latest
        depends_on: 
            - zookeeper
        ports: 
            - 9092:9092
        environment: 
            KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
            KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
            KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    
    db:
        image: postgres
        depends_on: 
            - kafka
        environment:
            POSTGRES_PASSWORD: "123"
        ports:
            - 5432:5432
            
```

`Spark`' ın `Kafka`' dan okuduğu verileri `PostgreSQL`' e yazabilmesi `postgresql jdbc jar`' ı gerekmektedir. Kullanıdığım jar' ı sisteminize indirmek için;

```
curl https://jdbc.postgresql.org/download/postgresql-42.2.5.jar --output postgresql-42.2.5.jar
```

Python için gerekli kütüphaneleri kurmak için;

```
pip3 install -r requirements.txt
```

### Çalışma Sistemi

![diagram](img/diagram.png)

Yukarıdaki resimde görüldüğü gibi `Spark`, `Kafka`' dan verileri okuyup `PostgreSQL`' e yazmaktadır.

Bu veri okuma ve yazma  işleminde `spark-shell` kullanılmaktadır. `spark-shell`, `consurmer.py`' ı çalıştırarak veri dönüştürme ve `PostgreSQL`' e yazma işlemini gerçekleştirmektedir.

`Spark`' tan okunan verilerin dönüştürüleceği `schema` değerleri `schemas.py` dosyasından `topic` adına göre elde edilir. Örneğin: schemas['order']. `consurmer.py` `schema`' yı `schemas.py` dosyasından elde eder.

`Spark`' tan okunan verilerin temizlenmesi işlemleri `transforms.py` dosyasından `topic` adına göre elde edilir. Örneğin: transforms['order'] işlemi order topic' ındeki orders.json verilerinin transfrom işlemini yapacak olan fonksiyonu return eder. `consumer.py`, verilerin dönüştürme işi için kullanılacak olan fonksiyonu `transforms.py`' dan bu şekilde elde eder.

`consumer.py`, `Spark`' ın bağlanacağı `Kafka` url' ini ve `Spark`' ın veri yazacağı `PostgreSQL` bağlantı bilgilerini `config.yml` dosyasından `config.py` sayesinde elde eder.

`consurmer.py`, hangi `topic`' ten veri okuyacağını(--topic) ve hangi tabloya(--table) yazacağını argümanlar ile elde eder.

Aşağıda klasör yapısını görebilirsiniz.

```bash
.
├── consumer.py
├── README.md
├── requirements.txt
└── src
    ├── config.py
    ├── config.yml
    ├── schemas.py
    └── trasforms.py

1 directory, 7 files
```

### Nasıl Çalıştırılır?

```
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 --driver-class-path postgresql-42.2.5.jar consumer.py --topic order --table orders
```


### Eksikler ve Hatalar

* Çok fazla Spark log' u olması
* Topic adına bağımlılığın olması
