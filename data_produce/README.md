## Data Product

Bu sistem `json` dosyalarını `Kafka`' ya belirli sürede bir yazan sistemdir.

### Kurulum

Öncelikle sisteminizde `Kafka` kurulu olmalıdır. Daha sonra gerekli `python` kütüphaneleri için;

```
    pip3 install -r requirements.txt
```

### Calisma Mantığı

![diagram](src/diagram.png)

`producer.py` kendisine verilen parametrelere göre `json` dosyasını okuyup, belirtilen `Kafka` `topic`' ine belirtilen sürede bir verileri yazar.

### Kullanım

```
    python3 producer.py --topic order --file src/data/orders.json --second 60

    python3 producer.py --topic product --file src/data/product-views.json --second 1
```


### Klasör yapısı
```bash
.
├── producer.py
├── README.md
├── requirements.txt
└── src
    ├── config.py
    ├── config.yml
    ├── data
    │   ├── orders.json
    │   └── product-views.json
    ├── diagram.png
    └── ndjson.py

2 directories, 9 files
```

