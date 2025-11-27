============================
Visualize Dokümantasyonu
============================

.. meta::
   :description: Visualize - Çeşitli veri dosyalarından interaktif grafik oluşturma aracı
   :keywords: python, görselleştirme, veri analizi, matplotlib, pandas

Visualize, çeşitli veri dosyalarından kolayca interaktif grafik oluşturmanıza olanak sağlayan güçlü bir Python komut satırı aracıdır.

.. contents:: İçindekiler
   :local:
   :depth: 2
   :backlinks: top

.. _genel-bakis:

📊 Genel Bakış
==============

Visualize, farklı formatlardaki veri dosyalarından interaktif grafik üretmek için geliştirilmiş bir komut satırı aracıdır. Veri görselleştirme işlemlerini kolaylaştırmak ve hızlandırmak amacıyla tasarlanmıştır.

Temel Özellikler
----------------

**Dosya İşleme Özellikleri:**

* ✅ **Çoklu Format Desteği**: CSV, Excel (XLSX/XLS), JSON ve TXT dosyaları
* ✅ **Otomatik Tip Algılama**: Dosya tipini otomatik olarak algılar
* ✅ **Metadata Görüntüleme**: Dosya boyutu, uzantı ve isim bilgilerini gösterir
* ✅ **Toplu İşleme**: Birden fazla dosyayı aynı anda işleyebilir
* ✅ **Akıllı Delimiter Tespiti**: TXT dosyaları için otomatik delimiter algılama

**Görselleştirme Tipleri:**

* 📈 **Çizgi Grafikleri (Line Chart)** - Zaman serisi ve trend analizi için ideal
* 📊 **Çubuk Grafikleri (Bar Chart)** - Kategorik veri karşılaştırmaları
* 📉 **Histogram** - Dağılım analizi [YAPIM AŞAMASINDA]
* 📋 **Tablo (Table)** - Verinin tablo formatında profesyonel görüntülenmesi

**İnteraktif Özellikler:**

* 🎯 Dosya seçimi için modern interaktif menü (InquirerPy)
* 🎨 Kolon seçimi arayüzü
* ⚙️ Grafik türü ve konfigürasyon seçenekleri
* 👀 Veri önizleme özelliği
* 🔄 Çoklu görselleştirme modları:
  
  - Tüm dosyalar için tek görselleştirme
  - Her dosya için ayrı görselleştirme
  - Dosyaları karşılaştırmalı görselleştirme

**Çıktı ve Dışa Aktarma:**

* 🖼️ İnteraktif görüntüleme (GUI backend mevcutsa)
* 💾 Yüksek çözünürlüklü PNG olarak kaydetme
* 🎨 Matplotlib tabanlı profesyonel kalitede grafikler

Desteklenen Dosya Formatları
-----------------------------

.. list-table::
   :widths: 20 30 50
   :header-rows: 1

   * - Format
     - Uzantılar
     - Açıklama
   * - CSV
     - ``.csv``
     - Virgülle ayrılmış değerler
   * - Excel
     - ``.xlsx``, ``.xls``
     - Microsoft Excel dosyaları (openpyxl ile)
   * - JSON
     - ``.json``
     - JavaScript Object Notation
   * - TXT
     - ``.txt``
     - Otomatik delimiter tespiti ile metin dosyaları

.. _kurulum:

⚙️ Kurulum
==========

Sistem Gereksinimleri
----------------------

* **Python** 3.10 veya üzeri
* **İşletim Sistemi**: Linux, macOS, Windows

Adım 1: Sanal Ortam Oluşturma
------------------------------

.. code-block:: bash

   python3 -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   # Windows için: .venv\Scripts\activate

Adım 2: Bağımlılıkları Yükleme
-------------------------------

.. code-block:: bash

   pip install -r requirments.txt

Temel bağımlılıklar:

* ``matplotlib`` - Grafik oluşturma motoru
* ``pandas`` - Veri işleme ve dosya okuma
* ``inquirerpy`` - İnteraktif CLI arayüzü
* ``openpyxl`` - Excel dosyası desteği

Adım 3: GUI Backend (Opsiyonel)
--------------------------------

Eğer grafiklerin ekranda interaktif olarak görüntülenmesini istiyorsanız, sisteminizde bir Matplotlib backend'i kurmalısınız:

**TkAgg Backend (Önerilen):**

.. code-block:: bash

   # Linux (Debian/Ubuntu)
   sudo apt install python3-tk

   # Linux (Fedora/RHEL)
   sudo dnf install python3-tkinter

   # Linux (Arch)
   sudo pacman -S tk

   # macOS
   brew install python-tk

   # Windows - Genellikle Python ile birlikte gelir

**Qt5Agg Backend (Alternatif):**

.. code-block:: bash

   pip install PyQt5

**GTK3Agg Backend (Linux):**

.. code-block:: bash

   # Debian/Ubuntu
   sudo apt install python3-gi

   # Fedora
   sudo dnf install python3-gobject

   # Arch
   sudo pacman -S python-gobject

.. note::
   Backend bulunamazsa, görseller otomatik olarak PNG dosyası olarak kaydedilir.

.. _hizli-baslangic:

🚀 Hızlı Başlangıç
==================

Programı Çalıştırma
-------------------

.. code-block:: bash

   python -m visualize.main

İnteraktif Menü Akışı
---------------------

Program aşağıdaki adımları takip eder:

1. **📁 Dosya Seçimi**
   
   * ``Space`` tuşu ile dosyaları seçin
   * Birden fazla dosya seçebilirsiniz
   * ``Enter`` ile onaylayın

2. **🎯 Görselleştirme Modu Seçimi**
   
   * ``Tüm dosyalar için aynı görselleştirme`` - Tek bir grafik tipi
   * ``Her dosya için farklı görselleştirme`` - Her dosya için ayrı grafik tipi
   * ``Dosyaları karşılaştırmalı görselleştirme`` - Yan yana karşılaştırma

3. **📊 Grafik Türü Seçimi**
   
   * Line Chart (Çizgi Grafiği)
   * Bar Chart (Çubuk Grafiği)
   * Table (Tablo Görünümü)

4. **🎨 Kolon Seçimi**
   
   * X ekseni kolonunu seçin
   * Y ekseni kolonunu seçin (grafik tiplerine göre)

5. **✏️ Grafik Başlığı**
   
   * İsteğe bağlı başlık belirleyin

.. _ornekler:

📝 Kullanım Örnekleri
=====================

Örnek 1: Tek Excel Dosyası - Çizgi Grafiği
-------------------------------------------

Zaman serisi verisi içeren bir Excel dosyasını görselleştirmek için:

.. code-block:: bash

   python -m visualize.main

**Adımlar:**

1. ``visualize/data/employees.xlsx`` dosyasını seçin
2. Görselleştirme modu: **"Tüm dosyalar için aynı"**
3. Grafik türü: **Line Chart**
4. X ekseni: Tarih/zaman kolonu (örn: ``Date``)
5. Y ekseni: Değer kolonu (örn: ``Sales``)
6. Başlık: ``"Aylık Satış Trendi"``

Örnek 2: Çoklu Dosya Karşılaştırma
-----------------------------------

Birden fazla CSV dosyasını karşılaştırmak için:

.. code-block:: bash

   python -m visualize.main

**Adımlar:**

1. ``Space`` tuşu ile ``data.csv`` ve ``products.txt`` dosyalarını seçin
2. Mod: **"Compare files side-by-side"**
3. Ortak kolonları görüntüleyin
4. Karşılaştırmak istediğiniz kolonları seçin
5. Yan yana grafikler oluşturulur

Örnek 3: JSON Dosyası - Tablo Görüntüleme
------------------------------------------

JSON formatındaki veriyi tablo olarak görüntülemek için:

.. code-block:: bash

   python -m visualize.main

**Adımlar:**

1. ``.json`` uzantılı dosyanızı seçin
2. Grafik türü: **Table**
3. Görüntülenecek satır sayısı: ``10`` (varsayılan)
4. Başlık: ``"Ürün Listesi"``

Örnek Veri Dosyaları
---------------------

Proje içerisinde ``visualize/data/`` klasöründe örnek veri dosyaları bulunmaktadır:

* ``data.csv`` - Genel CSV verisi örneği
* ``employees.xlsx`` - Çalışan bilgileri (Excel)
* ``products.txt`` - Ürün listesi (TXT formatında)

Klavye Kısayolları
------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Tuş
     - İşlev
   * - ``Space``
     - Seçim yapma (checkbox menülerinde)
   * - ``↑`` / ``↓``
     - Yukarı/Aşağı hareket
   * - ``Enter``
     - Seçimi onayla ve devam et
   * - ``q``
     - Çıkış veya iptal

.. _api-referansi:

🔧 API Referansı
================

Visualize modüler bir yapıya sahiptir. Her modül belirli bir sorumluluğa sahiptir:

visualize.main
--------------

Ana giriş noktası ve uygulama başlatıcı.

.. automodule:: visualize.main
   :members:
   :undoc-members:
   :show-inheritance:

visualize.engine
----------------

Ana motor ve koordinasyon katmanı. Tüm workflow'u yönetir.

.. automodule:: visualize.engine
   :members:
   :undoc-members:
   :show-inheritance:

visualize.cli
-------------

Komut satırı arayüzü ve kullanıcı etkileşimi modülü. InquirerPy kullanarak interaktif menüler sağlar.

.. automodule:: visualize.cli
   :members:
   :undoc-members:
   :show-inheritance:

visualize.file
--------------

Dosya işlemleri, okuma ve validasyon modülü. Çoklu format desteği sağlar.

.. automodule:: visualize.file
   :members:
   :undoc-members:
   :show-inheritance:

visualize.visualize
-------------------

Görselleştirme stratejileri ve grafik oluşturma modülü. Matplotlib kullanarak grafikler üretir.

.. automodule:: visualize.visualize
   :members:
   :undoc-members:
   :show-inheritance:

Mimari Genel Bakış
------------------

.. code-block:: text

   ┌─────────────┐
   │  main.py    │  ← Giriş noktası
   └──────┬──────┘
          │
          ▼
   ┌─────────────┐
   │  engine.py  │  ← Ana koordinatör
   └──────┬──────┘
          │
          ├────────────┬────────────┐
          ▼            ▼            ▼
   ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │  cli.py  │ │ file.py  │ │visualize.py  │
   └──────────┘ └──────────┘ └──────────────┘
   UI/Menü     Dosya İşleme   Grafik Üretimi

Modül Sorumlulukları
--------------------

**main.py**
   * Uygulama başlatma
   * Hata yakalama (top-level)

**engine.py**
   * Workflow koordinasyonu
   * Modüller arası iletişim
   * Ana iş mantığı

**cli.py**
   * Kullanıcı etkileşimi
   * İnteraktif menüler
   * Girdi validasyonu

**file.py**
   * Dosya okuma/yazma
   * Format dönüşümleri
   * Veri validasyonu

**visualize.py**
   * Grafik stratejileri
   * Matplotlib konfigürasyonu
   * Çıktı oluşturma

.. _sorun-giderme:

🛠️ Sorun Giderme
================

Backend Bulunamadı Hatası
-------------------------

**Hata Mesajı:**

.. code-block:: text

   UserWarning: No GUI backend found. Saving plots as PNG files.

**Çözüm:**

.. code-block:: bash

   # Linux (Ubuntu/Debian)
   sudo apt install python3-tk

   # veya
   pip install PyQt5

Excel Dosyası Okuma Hatası
--------------------------

**Hata Mesajı:**

.. code-block:: text

   ImportError: Missing optional dependency 'openpyxl'

**Çözüm:**

.. code-block:: bash

   pip install openpyxl

Encoding Hataları (Türkçe Karakterler)
---------------------------------------

**Hata Mesajı:**

.. code-block:: text

   UnicodeDecodeError: 'utf-8' codec can't decode byte...

**Çözüm:**

Dosyanızı UTF-8 encoding ile kaydedin veya farklı encoding belirtin.

Veri Formatı Hataları
---------------------

**Semptom:** Program dosyayı okuyamıyor veya kolonları bulamıyor.

**Çözümler:**

1. CSV dosyalarında delimiter'ı kontrol edin (``,`` veya ``;``)
2. İlk satırın başlık satırı olduğundan emin olun
3. Boş satırların olmadığını kontrol edin
4. JSON dosyalarında valid JSON formatı kullanın

.. _katkida-bulunma:

🤝 Katkıda Bulunma
==================

Bu proje açık kaynak kodludur ve katkılarınızı bekliyoruz!

GitHub Repository
-----------------

* **Repository**: https://github.com/riqoto/visual
* **Issues**: https://github.com/riqoto/visual/issues
* **Pull Requests**: https://github.com/riqoto/visual/pulls

Nasıl Katkıda Bulunulur?
------------------------

1. Repository'yi fork edin
2. Feature branch oluşturun (``git checkout -b feature/amazing-feature``)
3. Değişikliklerinizi commit edin (``git commit -m 'feat: Add amazing feature'``)
4. Branch'inizi push edin (``git push origin feature/amazing-feature``)
5. Pull Request açın

Kod Standartları
----------------

* **Docstrings**: Google style docstrings kullanın
* **Type Hints**: Mümkün olduğunca type annotation kullanın
* **Linting**: Code'unuzun PEP 8 uyumlu olduğundan emin olun

.. _lisans:

📄 Lisans ve İletişim
=====================

Lisans
------

Bu proje MIT lisansı altında yayınlanmıştır.

İletişim
--------

* **Geliştirici**: Riqoto
* **GitHub**: `@riqoto <https://github.com/riqoto>`_
* **Proje**: `Visualize <https://github.com/riqoto/visual>`_

.. _indeksler:

📑 İndeksler ve Tablolar
========================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

----

.. note::
   **Son Güncelleme:** 2024 | **Versiyon:** 1.0.0 | Made with ❤️ by Riqoto
