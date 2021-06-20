## Category Management

Bu modül `PostgreSQL`' e yazılan verileri kullanılarak aşağıdaki işlemleri gerçekleştirir;
1. Her bir kategori için, farklı kullanıcıların en fazla görüntülediği 10 ürünü
2. Her bir kategori için, farklı kullanıcıların en fazla satın aldığı 10 ürünü
3. Her bir kategori için (satın alınan / görünlenen) ürün oranı


## İçindekiler

* [Nasıl Kurulur](#nasıl-kurulur)
* [Çalışma Sistemi](#calisma-sistemi)
* [Nasıl Çalıştırılır](#nasıl-çalıştırılır)
* [Eksikler ve Hatalar](#eksikler-ve-hatalar)

### Nasıl kurulur?

Sistem veritabanı sorguları için `psycopg2` modülü kullanmaktadır. Bu modülü linux ortamında kullanmak için `libpq-dev`' i kurmamız gerekir.

```
sudo apt-get install libpq-dev
```

Sistemin çalışması için gerekli `python` kütüphanelerini ise aşağıdaki komutla kurabilirsiniz;

```
pip3 install -r requirements.txt
```

Sistemin düzgün çalışabilmesi için `product-category-map.csv` dosyasını `PostgreSQL`' e yazmamız gerekmektedir. Bu işlem için sisteminizde `Spark` olmalı. CSV dosyasını `PostgreSQL`' e yazmak için;
```
python3 src/utils/write_csv_to_postgre.py 
```

### Calisma Sistemi

![diagram](img/diagram.png)

Script' ler için gerekli olan sorgular `sql.py` dosyasından elde edelir.

Veritabanı bağlantısı `conn.py`' dan elde edilir.

Veritabanı bağlantısı için gereken şeyler `config.py` ile elde edilir.

Aşağıda klasör yapısını görebilirsiniz.

```bash
.
├── main.py
├── README.md
├── requirements.txt
└── src
    ├── category_bought.py
    ├── category_viewed.py
    ├── conversion_rates.py
    └── utils
        ├── config.py
        ├── conn.py
        ├── sql.py
        └── write_csv_to_postgre.py

2 directories, 10 files
```

### Nasıl çalıştırılır?

```
python3 main.py
```


### Eksikler ve Hatalar

1. Kod yazılım kötü