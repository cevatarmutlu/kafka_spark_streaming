## Hepsiburada Case

Hepsiburada' nın atmış olduğu case kodları.

Bana gönderdikleri verileri kullanarak benden istedikleri şeyler;

* Kategori yönetiminin saatlik olarak belirli dosya formatında istediği veriler
    * Herbir ürün kategorisi için farklı kullanıcılar tarafından en fazla görüntülenen 10 ürün.
    * Herbir ürün kategorisi için farklı kullanıcılar tarafından en fazla satın alınan 10 ürün.
    * Her bir ürün kategorisi için (satın alma / görüntülenme) sayısı

* Pazarlama departmanı için gerçek zamanlı analizler
    * Son 5 dakika içinde ürün görüntüleyen kullanıcılar
    * Son 5 dakika içinde ürün görüntülenen kategoriler
    * Son 5 dakika içinde ürün görüntülenen platformlar

* Kullanıcılara ürün tavsiye etmek için id numarasi verilen kullanıcının incelediği 5 ürünü dönen bir API

## Kullanılan Teknolojiler

Teknoloji   | Kullanımı
---------   | ---------
Linux       | Sistem Linux üzerinde kurulmuştur. Ubuntu dağıtımı
Kafka       | Sistemler için ortak veri platformu
PostgreSQL  | Temizlenen verilerin yazıldığı DB.
Docker      | Kafka ve PostgreSQL
Python3.8   | Sistemin yazıldığı dil
Spark       | Kafka' dan veriyi okuyup, temizleyip DB' ye yazmak için
Flask       | API yazabilmek için
SQLAlchemy  | API için veritabanı sorgularını daha kolay yapmak için kullanıldı
Pandas      | CSV dosyalarını oluşturmak için


## Çalışma Sistemi

![diagram](img/diagram.png)


### Modüller ve yaptığı işler


Modül | Yaptığı iş
----- | ----------
data_produce            | Gönderilen data dosyalarını Kafka' ya yazar.
data_consumer           | Kafka' dan veri okur ve PostgreSQL' e yazar
category_management     | DB' den verileri okuyarak kategori yönetimi için istenen csv dosyalarını elde eder.
marketing_department    | Pazarlama departmanının talep ettiği gerçek zamanlı analizler gerçekleştirir
api                     | Kullanıcılara ürün tavsiye etmek için belirli kullanıcının incelediği 5 ürünü döner


## Parçalı Anlatım

### data_produce

Bu sistem `ndjson` formatında verilmiş dosyaları, belirli sürede bir -mesela 5 saniyede bir- `Kafka`' ya yazmaya yarar. `Kafka`' ya yazılan veriler hiçbir temizleme işlemi olmadan olduğu gibi yazılmaktadır. 

[Daha Fazla bilgi ve kurulum](https://github.com/cevatarmutlu/hepsiburada_case/tree/master/code/data_produce)

### data_consumer

Bu sistem `Kafka`' daki belirli `topic`' lerde bulunan veriyi `Spark streaming` okur, okuduğu veriyi temizleyerek `postgreSQL` veritabanındaki belirli tablolara yazar.

[Daha Fazla bilgi ve kurulum](https://github.com/cevatarmutlu/hepsiburada_case/tree/master/code/data_consumer)


### category_management

Bu modül `PostgreSQL`' e yazılan orders ve product-views verileri kullanılarak aşağıdaki işlemler gerçekleştirir;
1. farklı kullanıcıların, her bir kategoride en fazla görüntülediği 10 ürünü
2. farklı kullanıcıların, her bir kategoride en fazla satın alıdığı 10 ürünü
3. her kategiri için (satın alınan / görünlenen) oranı

Çalışma şekli aşağıdaki gibidir:

![req1-diagram](img/req1-diagram.png)

******************************************
/*Buraya screnshot' ler gelecek*/
******************************************

[Daha Fazla bilgi ve kurulum](https://github.com/cevatarmutlu/hepsiburada_case/tree/master/code/req1)

### marketing_department

Bu modül `Kafka`' ya yazılan product-views verileri kullanılarak real-time olarak aşağıdaki işlemleri gerçekleştirir;
1. Son 5 dakika içinde herhangi bir ürünü görüntüleyen kullanıcılar
2. Son 5 dakika içinde görüntülenen ürünlerin kategorileri
3. Son 5 dakika içinde görüntülenen ürünlerin platformları

[Daha Fazla bilgi ve kurulum](https://github.com/cevatarmutlu/hepsiburada_case/tree/master/code/req2)


### api

Bu modül kendine verilen kullanıcın görüntülediği en son 5 ürünü dönen bir API' dır.

[Daha Fazla bilgi ve kurulum](https://github.com/cevatarmutlu/hepsiburada_case/tree/master/code/api)