## Marketing Department

Bu modül `Kafka`' ya yazılan product-views verileri kullanılarak real-time olarak aşağıdaki işlemleri gerçekleştirir;
1. Son 5 dakika içinde herhangi bir ürünü görüntüleyen kullanıcılar
2. Son 5 dakika içinde görüntülenen ürünlerin kategorileri
3. Son 5 dakika içinde görüntülenen ürünlerin platformları


## İçindekiler

* [Nasıl Kurulur](#nasıl-kurulur)
* [Çalışma Sistemi](#calisma-sistemi)
* [Nasıl Çalıştırılır](#nasıl-çalıştırılır)
* [Eksikler ve Hatalar](#eksikler-ve-hatalar)

### Nasıl kurulur?

Sistemin çalışması için gerekli `python` kütüphanelerini ise aşağıdaki komutla kurabilirsiniz;

```
pip3 install -r requirements.txt
```

### Calisma Sistemi

`consurmer.py` `Kafka`' dan verileri okur. Eğer ürünün görüntülenme tarihi 5 dakikadan önce bir tarih değilse -bazen önce olabiliyor- görüntülenme tarihi `timestamps` adlı bir diziye, kullanıcı `active_users` adlı bir diziye, platform değeri `platforms` adlı bir diziye eklenir.

`timestamps` dizinin boyutu 0' dan büyükse `timestamps` dizisindeki ilk index değerinin `timestamp` değerine bakılır. Eğer 5 dakikadan önce bir tarihse ilk index değeri diğer bütün dizilerden çıkartılır.

Elde verileri bir pandas DataFrame' ine dönüştürülür ve print edilir.

Aşağıda klasör yapısını görebilirsiniz.

```bash
.
├── consumer.py
├── README.md
├── requirements.txt
└── src
    ├── config.py
    ├── config.yml
    ├── product-category-map.csv

2 directories, 7 files
```

### Nasıl çalıştırılır?

```
python3 consurmer.py
```


### Eksikler ve Hatalar

1. Kod yazımı kötü
