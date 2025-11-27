"""Komut satırı arayüzü (CLI) modülü.

Bu modül, Visualize uygulamasının kullanıcı etkileşim katmanını sağlar.
InquirerPy kütüphanesi kullanılarak interaktif dosya seçimi, ASCII banner
gösterimi ve görselleştirme workflow'unun başlatılması gerçekleştirilir.

Classes:
    CLIConfig: CLI konfigürasyon ayarları (path, recursive, max_file).
    CLIError: CLI işlemleri sırasında oluşabilecek hata mesajları.
    CLI: Ana CLI uygulama sınıfı, kullanıcı etkileşimini yönetir.

Example:
    Temel kullanım::

        from cli import CLI, CLIConfig
        
        # Konfigürasyon oluştur
        config = CLIConfig(path="./my_data")
        
        # CLI başlat ve çalıştır
        cli = CLI(config)
        cli.run()
"""

import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from file import File
from InquirerPy import inquirer

from visualize import VisualizationWorkflow


@dataclass
class CLIConfig:
    """CLI konfigürasyon ayarları.
    
    Bu dataclass, CLI uygulamasının çalışma parametrelerini saklar.
    Veri klasörü yolu, recursive tarama ve maksimum dosya sayısı gibi
    ayarları içerir.
    
    Attributes:
        path (str): Veri dosyalarının bulunduğu klasör yolu.
            Varsayılan "./data".
        recursive (bool): Alt klasörlere de bakılıp bakılmayacağı.
            Varsayılan False. (ŞU AN IMPLEMENT EDİLMEMİŞ)
        max_file (int): Listelenecek maksimum dosya sayısı.
            Varsayılan 100.
    
    Raises:
        SystemExit: Path mevcut değilse __post_init__() içinde çıkış yapar.
    
    Example:
        >>> config = CLIConfig(path="./mydata", max_file=50)
        >>> print(config.path)
        ./mydata
    
    Todo:
        * Recursive klasör taraması implement edilecek
        * getcwd() kullanarak current path default olarak ayarlanacak
    """

    path: str = "./data"
    """Veri dosyalarının bulunduğu klasör yolu. Varsayılan ./data"""
    
    recursive: bool = False
    """Alt klasörlerin de taranıp taranmayacağı. ŞU AN AKTİF DEĞİL."""
    
    max_file: int = 100
    """Liste lenecek maksimum dosya sayısı."""

    def __post_init__(self):
        """Konfigürasyon validasyonu yapar.
        
        Path'in var olup olmadığını kontrol eder. Yoksa program sonlandırılır.
        
        Raises:
            SystemExit: Belirtilen path mevcut değilse.
        
        Example:
            >>> config = CLIConfig(path="/nonexistent")
            >>> # SystemExit fırlatılır
        """
        if not os.path.exists(self.path):
            sys.exit(f"An Error occur: {self.path} {CLIError.PathDoesntExist.value}")


class CLIError(Enum):
    """CLI işlemleri sırasında oluşabilecek hata mesajları.
    
    Bu enum, CLI katmanında karşılaşılan standart hata durumlarını tanımlar.
    Kullanıcıya anlamlı mesajlar göstermek için kullanılır.
    
    Attributes:
        DataNotFound (str): Veri bulunamadı hatası.
        PathDoesntExist (str): Belirtilen yol bulunamadı hatası.
        FolderIsEmpty (str): Klasör hiç dosya içermiyor hatası.
        FileIsNotValid (str): Dosya geçerli değil hatası.
        FolderDoesntHaveValidFileTypes (str): Klasörde desteklenen 
            format yoksa hatası.
    """

    DataNotFound = "data not found"
    PathDoesntExist = "path does not exist"
    FolderIsEmpty = "folder does not include any file"
    FileIsNotValid = "file is not valid"
    FolderDoesntHaveValidFileTypes = (
        "Folder do not include valid file types for visualize"
    )


class CLI(CLIConfig):
    """Ana CLI uygulama sınıfı.
    
    Kullanıcı etkileşimini yöneten ana sınıf. ASCII banner gösterimi,
    dosya seçimi, validasyon ve görselleştirme workflow'unu başlatma
    sorumluluğuna sahiptir.
    
    Attributes:
        config (CLIConfig): CLI konfigürasyon ayarları.
        project_link (str): GitHub repository linki.
    
    Example:
        >>> config = CLIConfig(path="./data")
        >>> cli = CLI(config)
        >>> cli.run()  # İnteraktif workflow başlar
    """

    def __init__(self, config: CLIConfig):
        """CLI sınıfını başlatır.
        
        Args:
            config (CLIConfig): Validate edilmiş CLI konfigürasyonu.
        
        Note:
            CLIConfig'de __post_init__() çağrılmış olmalıdır.
        """
        self.config = config
        self.project_link: str = "https://www.github.com/riqoto/visual"

    def create_files_prompt(self) -> list[str]:
        """Kullanıcıya dosya seçimi için interaktif menü gösterir.
        
        InquirerPy checkbox kullanarak birden fazla dosya seçimine izin verir.
        En az 1 dosya seçilmesi zorunludur.
        
        Returns:
            list[str]: Seçilen dosya isimleri listesi.
        
        Raises:
            SystemExit: Kullanıcı 'q' ile çıkış yaparsa veya beklenmeyen hata olursa.
        
        Example:
            >>> cli = CLI(config)
            >>> selected = cli.create_files_prompt()
            >>> print(selected)
            ['data.csv', 'employees.xlsx']
        
        Note:
            - Space tuşu ile dosya seçilir
            - Enter ile onaylanır
            - 'q' ile çıkış yapılır
            - En az 1 dosya seçilmesi zorunludur
        """
        files = []
        try:
            files = inquirer.checkbox(
                message="Select file/files to visualize [press space for selection]",
                choices=[file for file in self.get_files()],
                validate=lambda result: len(result) >= 1,
                invalid_message="Please select one file or more",
                border=True,
                qmark="📄",
                keybindings={
                    "interrupt": [{"key": "q"}],  # raise KeyboardInterrupt
                },
            ).execute()
        except KeyboardInterrupt:
            sys.exit("User Exit")
        except Exception as e:
            sys.exit(f"Unexpected Error: {str(e)}")

        # Validation menüde zaten var, bu yüzden liste boş olamaz
        # Kullanıcı ya çıkış yapar ya da en az 1 dosya seçer
        return files

    def get_files(self) -> list[str]:
        """Konfigüre edilmiş klasördeki tüm dosyaları listeler.
        
        Alt klasörlere bakmaz, sadece verilen path'teki dosyaları listeler.
        
        Returns:
            list[str]: Dosya isimleri listesi (sadece isimler, full path değil).
        
        Raises:
            SystemExit: Klasör boşsa veya okuma hatası oluşursa.
        
        Example:
            >>> cli = CLI(CLIConfig(path="./data"))
            >>> files = cli.get_files()
            >>> print(files)
            ['data.csv', 'employees.xlsx', 'products.json']
        
        Note:
            Sadece dosyaları listeler, alt klasörleri filtreleyerek atar.
        """
        try:
            all_items = os.listdir(self.config.path)

            # Filter only files (not directories)
            files_list = [
                item
                for item in all_items
                if os.path.isfile(os.path.join(self.config.path, item))
            ]

            if len(files_list) == 0:
                sys.exit(
                    f"An error occur: {self.config.path} {CLIError.FolderIsEmpty.value}"
                )

            return files_list

        except Exception as e:
            sys.exit(f"Error reading directory: {str(e)}")

    def intro(self):
        """ASCII banner ve uygulama bilgilerini konsola yazdırır.
        
        Visualize ASCII logosu, GitHub linki, taranacak klasör ve
        kullanım talimatlarını gösterir.
        
        Example:
            >>> cli.intro()
               ╦  ╦╦╔═╗╦ ╦╔═╗╦  ╦╔═╗╔═╗
               ╚╗╔╝║╚═╗║ ║╠═╣║  ║╔═╝║╣
                ╚╝ ╩╚═╝╚═╝╩ ╩╩═╝╩╚═╝╚═╝
            ...
        
        Note:
            Bu method sadece yazdırma yapar, herhangi bir işlem yapmaz.
        """
        banner = r"""
           ╦  ╦╦╔═╗╦ ╦╔═╗╦  ╦╔═╗╔═╗
           ╚╗╔╝║╚═╗║ ║╠═╣║  ║╔═╝║╣
            ╚╝ ╩╚═╝╚═╝╩ ╩╩═╝╩╚═╝╚═╝
                   """

        subtitle = "Visualize is a toolchain for data visualization"
        separator = "=" * 50
        github_info = f"GitHub: {self.project_link}"
        actions = (
            "\tFor selection press [Space]\n"
            + "\tFor move press [Up] or [Down]\n"
            + "\tFor answer press [Enter]\n"
            + "\tFor exit press [q]\n"
        )
        print("\n" + banner)
        print(f"{subtitle:^50}")
        print(separator)
        print(f"{github_info:^50}")
        print(separator + "\n")
        print(f"📁 Scanning directory: {self.config.path}")
        print(f"Actions:\n{actions:^50}")

    def visualize_files(self, file_names: list[str]):
        """Seçilen dosyalar için görselleştirme workflow'unu başlatır.
        
        Dosya isimlerini full path'e çevirir, validate eder ve geçerli
        olanlar için VisualizationWorkflow'u başlatır.
        
        Args:
            file_names (list[str]): Kullanıcının seçtiği dosya isimleri
                (config.path'e relative).
        
        Raises:
            SystemExit: Hiçbir geçerli dosya yoksa.
        
        Example:
            >>> cli.visualize_files(['data.csv', 'employees.xlsx'])
            ✅ 2 valid file(s) ready for visualization
            🚀 Starting visualization...
        
        Note:
            Geçersiz dosyalar atlanır, kullanıcıya uyarı gösterilir.
            En az 1 geçerli dosya olmalıdır.
        
        Todo:
            Tüm mantık burada, daha modüler hale getirilmeli.
        """
        # Convert file names to full paths
        full_paths = [
            os.path.join(self.config.path, file_name) for file_name in file_names
        ]

        # Validate all files
        valid_files = []
        for file_path in full_paths:
            try:
                file = File(file_path)
                file.__post_init__()  # Validate file
                if file.validate_suffix():
                    valid_files.append(file_path)
                else:
                    print(
                        f"⚠️  Skipping {Path(file_path).name}: {CLIError.FileIsNotValid}"
                    )
            except Exception as e:
                print(f"⚠️  Skipping {Path(file_path).name}: {str(e)}")

        if not valid_files:
            sys.exit(f"{CLIError.FolderDoesntHaveValidFileTypes.value}")
            return

        print(f"\n✅ {len(valid_files)} valid file(s) ready for visualization")

        # Start visualization workflow
        workflow = VisualizationWorkflow()
        workflow.run_with_shared_config(valid_files)

    def run(self):
        """CLI uygulamasını çalıştırır (ana entry point).
        
        Tam workflow:
        1. Intro banner göster
        2. Kullanıcıdan dosya seçimi al
        3. Seçilen dosyaları göster
        4. Görselleştirme workflow'unu başlat
        
        Raises:
            SystemExit: Kullanıcı dosya seçmez veya 'q' ile çıkış yaparsa.
        
        Example:
            >>> config = CLIConfig(path="./data")
            >>> cli = CLI(config)
            >>> cli.run()  # İnteraktif akış başlar
        
        Note:
            Bu method interaktif olarak çalışır, kullanıcı input'u bekler.
        """
        self.intro()

        selected_files = self.create_files_prompt()

        if selected_files:
            print(f"\n✅ Selected {len(selected_files)} file(s):")
            for f in selected_files:
                print(f"   📄 {f}")
            print("\n🚀 Starting visualization...\n")

            # Start visualization
            self.visualize_files(selected_files)

        else:
            sys.exit("\n⚠️  No file selected. Exiting...\n")
