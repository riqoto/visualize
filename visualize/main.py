"""Visualize - Veri Görselleştirme Aracı.

Bu modül Visualize uygulamasının giriş noktasıdır. CLI sınıfını başlatır
ve kullanıcı etkileşimli veri görselleştirme workflow'unu başlatır.

Example:
    Programı çalıştırmak için::

        $ python -m visualize.main

    veya doğrudan::

        $ python visualize/main.py

Note:
    Bu dosya direkt olarak çalıştırılmalıdır. Başka modüller tarafından
   import edilmesi amaçlanmamıştır.

Attributes:
    cli_config (CLIConfig): CLI konfigürasyon nesnesi, varsayılan veri yolunu içerir.
    cli (CLI): Ana CLI uygulama nesnesi.
"""

from cli import CLI, CLIConfig

if "__main__" == __name__:
    # Varsayılan veri klasörü ile CLI yapılandırması oluştur
    cli_config: CLIConfig = CLIConfig(path="/home/bhh/Belgeler/visiual/visualize/data")
    
    # CLI uygulamasını başlat
    cli: CLI = CLI(cli_config)
    
    # İnteraktif workflow'u çalıştır
    cli.run()
