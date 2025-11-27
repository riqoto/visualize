API Referansı
=============

Bu sayfada Visualize projesinin tüm modüllerinin detaylı API dokümantasyonunu bulabilirsiniz.

visualize.cli modülü
--------------------

Komut satırı arayüzü ve kullanıcı etkileşimi fonksiyonları. Bu modül, kullanıcıdan dosya seçimini
almak, interaktif promptlar göstermek ve görselleştirme workflow'unu başlatmak için gerekli tüm
araçları içerir.

**Ana Sınıflar:**

* ``CLIConfig`` - CLI konfigürasyon ayarları (varsayılan data klasörü, max dosya sayısı)
* ``CLI`` - Ana CLI sınıfı, interaktif menüler ve dosya seçimi
* ``CLIError`` - CLI hata mesajları enum'u

.. automodule:: visualize.cli
   :members:
   :undoc-members:
   :show-inheritance:

visualize.file modülü
---------------------

Dosya işlemleri, format tespiti ve veri okuma fonksiyonları. Desteklenen formatlar: CSV, Excel 
(XLSX/XLS), JSON ve TXT.

**Ana Sınıflar:**

* ``FileExtension`` - Desteklenen dosya uzantıları enum'u (CSV, XLSX, XLS, JSON, TXT)
* ``File`` - Dosya metadata ve validasyon sınıfı
* ``FileHandler`` - Dosya okuma ve pandas DataFrame dönüşümü
* ``FileError`` - Dosya işleme hataları enum'u

.. automodule:: visualize.file
   :members:
   :undoc-members:
   :show-inheritance:

visualize.visualize modülü
--------------------------

Görselleştirme stratejileri, grafik oluşturma ve interaktif workflow yönetimi. Strategy pattern
kullanılarak farklı grafik tipleri için ayrı sınıflar içerir.

**Ana Sınıflar:**

* ``VisualizationType`` - Mevcut görselleştirme tipleri enum'u (Line, Bar, Histogram, Table)
* ``VisualizationStrategy`` - Abstract base class, tüm görselleştirme stratejileri için temel
* ``LineChartStrategy`` - Çizgi grafikleri için implementasyon
* ``BarChartStrategy`` - Çubuk grafikleri için implementasyon
* ``HistogramStrategy`` - Histogram için implementasyon
* ``TableStrategy`` - Tablo görüntüleme için implementasyon
* ``VisualizationHandler`` - Görselleştirme yönetimi ve kullanıcı interaksiyonu
* ``VisualizationWorkflow`` - Çoklu dosya workflow'u ve karşılaştırma modları

.. automodule:: visualize.visualize
   :members:
   :undoc-members:
   :show-inheritance:

visualize.engine modülü
-----------------------

Ana motor ve koordinasyon sınıfı. Dosya işleme ile görselleştirme arasında köprü görevi görür.

**Ana Sınıflar:**

* ``VisiualEngine`` - Tüm bileşenleri bir araya getiren ana motor sınıfı

.. automodule:: visualize.engine
   :members:
   :undoc-members:
   :show-inheritance:

visualize.main modülü
---------------------

Ana giriş noktası ve program başlatma. CLI konfigürasyonunu yaratır ve çalıştırır.

.. automodule:: visualize.main
   :members:
   :undoc-members:
   :show-inheritance:

