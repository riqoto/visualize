# Visualize

Bu proje, CSV dosyalarından grafik üretmek için hazırlanmış basit bir
komut satırı aracıdır. `engine.py` ve `visualize.py` dosyaları temel
akışı yönetir.

## Kurulum

1.  Sanal ortam oluşturun:

    ``` bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  Bağımlılıkları yükleyin:

    ``` bash
    pip install -r requirments.txt
    ```

3.  Eğer grafiklerin ekranda açılmasını istiyorsanız sisteminizde bir
    Matplotlib backend'i bulunmalıdır (Tk, Qt veya GTK). Backend
    bulunamazsa görseller dosya olarak kaydedilir.

## Notlar

-   CSV içeriğine göre kolon seçimi ve grafik türü komut satırı
    üzerinden sorulacaktır.
-   Kod Python 3.10+ gerektirir.
