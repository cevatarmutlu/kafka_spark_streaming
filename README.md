## Hepsiburada Case

Hepsiburada' nın atmış olduğu case kodları.

## Kullanılan Teknolojiler

1. Kafka
2. PostgreSQL
3. Docker -> Kafka ve PostgreSQL
4. Python3.8
5. Spark Streaming -> Verileri temizleyip PostgreSQL' e yazmak için
6. Flask -> API için.
7. SQLAlchemy -> API sorguları için

## Çalışma Sistemi

![diagram](img/diagram.png)

* data_produce: Kafka' ya veri yazar.
* data_consumer: Kafka' dan veri okur PostgreSQL' e yazar
* req-1: DB' den verileri okuyarak csv dosyalarını elde eder.
* req-2: Kafka' dan veri okuyarak realtime olaral verileri print eder
* API ise kendisine verileren user' ın görüntülediği son 5 ürünü response eder.

## Parçalı Anlatım

### data_produce

Bu sistem `ndjson` formatında verilmiş dosyaları, belirli sürede bir -mesela 5 saniyede bir- `Kafka`' ya yazmaya yarar. `Kafka`' ya yazılan veriler hiçbir temizleme işlemi olmadan olduğu gibi yazılmaktadır. 

[Daha Fazla bilgi ve kurulum](tree/master/code/data_produce)


### req-1

Bu modül `PostgreSQL`' e yazılan orders ve product-views verileri kullanılarak aşağıdaki işlemler gerçekleştirir;
1. farklı kullanıcıların, her bir kategoride en fazla görüntülediği 10 ürünü
2. farklı kullanıcıların, her bir kategoride en fazla satın alıdığı 10 ürünü
3. her kategiri için (satın alınan / görünlenen) oranı

Çalışma şekli aşağıdaki gibidir:

![req1-diagram](img/req1-diagram.png)

******************************************
/*Buraya screnshot' ler gelecek*/
******************************************

### req-2

Bu modül `Kafka`' ya yazılan product-views verileri kullanılarak real-time olarak aşağıdaki işlemleri gerçekleştirir;
1. Son 5 dakika içinde herhangi bir ürünü görüntüleyen kullanıcılar
2. Son 5 dakika içinde görüntülenen ürünlerin kategorileri
3. Son 5 dakika içinde görüntülenen ürünlerin platformları

### api

Bu modül kendine verilen kullanıcın görüntülediği en son 5 ürünü dönen bir API' dır.