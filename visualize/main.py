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

import sys
import os

# Modül import sorunlarını çözmek için path ayarı
# Hem 'python -m visualize.main' hem de 'python visualize/main.py' çalışmasını sağlar
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

try:
    from cli import CLI, CLIConfig
except ImportError:
    # Fallback for module execution
    from visualize.cli import CLI, CLIConfig

if "__main__" == __name__:
    # Varsayılan veri klasörü ile CLI yapılandırması oluştur
    # Veri klasörü visualize/data altında varsayılıyor
    data_path = os.path.join(current_dir, "data")
    
    cli_config: CLIConfig = CLIConfig(path=data_path)
    
    # CLI uygulamasını başlat
    cli: CLI = CLI(cli_config)
    
    # İnteraktif workflow'u çalıştır
    cli.run()
