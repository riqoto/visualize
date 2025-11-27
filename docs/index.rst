Visualize Dokümantasyonu
========================

Visualize, çeşitli veri dosyalarından kolayca grafik oluşturmanıza olanak sağlayan güçlü bir Python komut satırı aracıdır.

.. toctree::
   :maxdepth: 2
   :caption: İçindekiler:

   api

Genel Bakış
-----------

Bu proje, farklı formatlardaki veri dosyalarından interaktif grafik üretmek için geliştirilmiş bir komut satırı aracıdır. 
Veri görselleştirme işlemlerini kolaylaştırmak ve hızlandırmak amacıyla tasarlanmıştır.

Desteklenen Dosya Formatları
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **CSV** (.csv) - Virgülle ayrılmış değerler
* **Excel** (.xlsx, .xls) - Microsoft Excel dosyaları
* **JSON** (.json) - JavaScript Object Notation
* **TXT** (.txt) - Metin dosyaları (otomatik delimiter tespiti ile)

Özellikler
~~~~~~~~~~

**Dosya İşleme:**

* Çoklu dosya formatı desteği (CSV, Excel, JSON, TXT)
* Otomatik dosya tipi algılama
* Dosya metadata görüntüleme (boyut, uzantı, isim)
* Çoklu dosya seçimi ve toplu işleme
* Otomatik delimiter tespiti (TXT dosyaları için)

**Görselleştirme Tipleri:**

* **Çizgi Grafikleri (Line Chart)** - Zaman serisi ve trend analizi
* **Çubuk Grafikleri (Bar Chart)** - Kategorik veri karşılaştırmaları
* **Histogram** - Dağılım analizi [YAPIM AŞAMASINDA]
* **Tablo (Table)** - Verinin tablo formatında görüntülenmesi

**İnteraktif Özellikler:**

* Dosya seçimi için interaktif menü
* Kolon seçimi arayüzü
* Grafik türü seçimi
* Grafik başlığı ve konfigürasyon özelleştirme
* Veri önizleme
* Çoklu görselleştirme modu:
  - Tüm dosyalar için aynı görselleştirme
  - Her dosya için farklı görselleştirme
  - Dosyaları karşılaştırmalı görselleştirme

**Çıktı Seçenekleri:**

* İnteraktif görüntüleme (GUI backend mevcutsa)
* Dosyaya kaydetme (PNG, yüksek çözünürlük)
* Matplotlib tabanlı profesyonel grafikler

Kurulum
--------

1. Sanal ortam oluşturun:

   .. code-block:: bash

      python3 -m venv .venv
      source .venv/bin/activate

2. Bağımlılıkları yükleyin:

   .. code-block:: bash

      pip install -r requirments.txt

3. **Opsiyonel - GUI Backend:** Eğer grafiklerin ekranda görüntülenmesini istiyorsanız sisteminizde bir Matplotlib backend'i bulunmalıdır:

   **TkAgg Backend (Önerilen):**

   * **Linux (Debian/Ubuntu)**: ``sudo apt install python3-tk``
   * **Linux (Fedora/RHEL)**: ``sudo dnf install python3-tkinter``
   * **Linux (Arch)**: ``sudo pacman -S tk``
   * **macOS**: ``brew install python-tk``
   * **Windows**: Tk genellikle Python ile birlikte gelir

   **Qt5Agg Backend (Alternatif):**

   * **Tüm Platformlar**: ``pip install PyQt5``

   **GTK3Agg Backend (Linux):**

   * **Debian/Ubuntu**: ``sudo apt install python3-gi``
   * **Fedora**: ``sudo dnf install python3-gobject``
   * **Arch**: ``sudo pacman -S python-gobject``

   Backend bulunamazsa görseller otomatik olarak PNG dosyası olarak kaydedilir.

Hızlı Başlangıç
---------------

Basit Kullanım
~~~~~~~~~~~~~~

Programı çalıştırmak için:

.. code-block:: bash

   python -m visualize.main

Program sizden:

1. **Dosya seçimi** yapmanızı isteyecek (Space ile seçim, Enter ile onay)
2. **Görselleştirme modu** seçmenizi isteyecek:
   
   * Tüm dosyalar için aynı görselleştirme
   * Her dosya için farklı görselleştirme
   * Dosyaları karşılaştırmalı görselleştirme

3. **Grafik türü** seçmenizi isteyecek (Çizgi, Çubuk, Tablo)
4. **Kolon seçimi** yapmanızı isteyecek (X ekseni, Y ekseni)
5. **Grafik başlığı** belirlemenizi isteyecek

Seçimlerinize göre grafik otomatik olarak oluşturulacaktır.

Kullanım Örnekleri
------------------

Örnek 1: Tek Dosya - Çizgi Grafiği
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Zaman serisi verisi içeren bir Excel dosyanız varsa:

.. code-block:: bash

   python -m visualize.main

1. ``visualize/data/`` klasöründen ``employees.xlsx`` dosyasını seçin
2. Görselleştirme modu olarak "Tüm dosyalar için aynı" seçin
3. Grafik türü olarak **Line Chart** seçin
4. X ekseni için tarih/zaman kolonunu seçin
5. Y ekseni için değer kolonunu seçin
6. Grafik başlığını belirleyin

Örnek 2: Çoklu Dosya Karşılaştırma
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Birden fazla veri dosyasını karşılaştırmak için:

.. code-block:: bash

   python -m visualize.main

1. Space tuşu ile birden fazla dosya seçin (örn: ``data.csv`` ve ``products.txt``)
2. **"Compare files side-by-side"** modunu seçin
3. Ortak kolonları görüntüleyin
4. Karşılaştırmak istediğiniz kolonları seçin

Örnek 3: JSON Dosyası - Tablo Görüntüleme
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSON formatındaki veriyi tablo olarak görüntülemek için:

.. code-block:: bash

   python -m visualize.main

1. ``.json`` uzantılı dosyanızı seçin
2. Grafik türü olarak **Table** seçin
3. Görüntülenecek satır sayısını belirleyin (varsayılan: 10)
4. Tablo başlığını yazın

Örnek Veri Dosyaları
~~~~~~~~~~~~~~~~~~~~~

Proje içerisinde ``visualize/data/`` klasöründe örnek veri dosyaları bulunmaktadır:

* ``data.csv`` - CSV örneği
* ``employees.xlsx`` - Excel örneği
* ``products.txt`` - TXT örneği

Klavye Kısayolları
------------------

Program boyunca kullanılabilecek klavye kontrolleri:

* **Space** - Seçim yapma (checkbox menülerinde)
* **↑/↓** - Yukarı/Aşağı hareket
* **Enter** - Seçimi onayla
* **q** - Çıkış/İptal

API Dokümantasyonu
------------------

Detaylı modül ve sınıf dokümantasyonu için :doc:`api` sayfasına bakın.

Mimari ve Modüller
------------------

Proje modüler bir yapıya sahiptir:

* ``cli.py`` - Komut satırı arayüzü ve kullanıcı etkileşimi
* ``file.py`` - Dosya işlemleri, okuma ve validasyon
* ``visualize.py`` - Görselleştirme stratejileri ve workflow
* ``engine.py`` - Ana motor ve koordinasyon
* ``main.py`` - Giriş noktası

Gereksinimler
-------------

* **Python** 3.10 veya üzeri
* **Matplotlib** - Grafik oluşturma
* **Pandas** - Veri işleme ve dosya okuma
* **InquirerPy** - İnteraktif CLI arayüzü
* **openpyxl** - Excel dosyası okuma (pandas tarafından kullanılır)

Sorun Giderme
-------------

Backend Hatası
~~~~~~~~~~~~~~

Eğer "No GUI backend found" hatası alıyorsanız:

.. code-block:: bash

   sudo apt install python3-tk

Dosya Okuma Hatası
~~~~~~~~~~~~~~~~~~

Eğer Excel dosyası okuma hatası alıyorsanız:

.. code-block:: bash

   pip install openpyxl

Katkıda Bulunma
---------------

Bu proje açık kaynak kodlu bir projedir. GitHub repository'si: https://www.github.com/riqoto/visual

İndeksler ve Tablolar
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

