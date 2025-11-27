"""Dosya işlemleri ve veri okuma modülü.

Bu modül, çeşitli formatlardaki veri dosyalarının (CSV, Excel, JSON, TXT)
okunması, validasyonu ve metadata çıkarımı için gerekli sınıfları içerir.

Pandas kütüphanesi kullanılarak dosyalar D ataFrame'e dönüştürülür ve
görselleştirme için hazır hale getirilir.

Classes:
    FileExtension: Desteklenen dosya uzantıları enum'u.
    FileError: Dosya işlemi hataları enum'u.
    File: Dosya nesnesi ve validasyon işlemleri.
    FileHandler: Dosya okuma ve veri işleme operasyonları.

Example:
    Temel kullanım::

        from file import File, FileHandler
        
        # Dosya oluştur ve validate et
        file = File("/path/to/data.csv")
        file.__post_init__()
        
        # Dosyayı oku
        handler = FileHandler(file)
        data = handler.read_file()
        
        # Veri önizlemesi
        handler.preview_data(rows=10)
"""

import sys
from enum import Enum
from pathlib import Path

import pandas as pd


class FileExtension(Enum):
    """Veri analizi için desteklenen dosya uzantıları.
    
    Bu enum, Visualize uygulamasının desteklediği tüm dosya formatlarını
    tanımlar. Her format için dosya uzantısı string olarak saklanır.
    
    Attributes:
        CSV (str): Virgülle ayrılmış değerler (.csv).
        EXCEL (str): Modern Excel formatı (.xlsx).
        EXCEL_OLD (str): Eski Excel formatı (.xls).
        JSON (str): JavaScript Object Notation (.json).
        TXT (str): Metin dosyaları, delimiter otomatik tespit edilir (.txt).
    
    Note:
        Bu enum proje spesifiktir ve tüm dosya formatlarını kapsamaz.
        Yeni format eklendiğinde buraya eklenmeli ve FileHandler.read_file()
        metodunda da implement edilmelidir.
    """

    CSV = ".csv"
    EXCEL = ".xlsx"
    EXCEL_OLD = ".xls"
    JSON = ".json"
    TXT = ".txt"


class FileError(Enum):
    """Dosya işlemleri sırasında oluşabilecek hata mesajları.
    
    Bu enum, dosya validasyonu ve okuma sırasında karşılaşılabilecek
    standart hata durumlarını tanımlar.
    
    Attributes:
        FileDoesntExist (str): Dosya bulunamadı hatası.
        NotFile (str): Path bir dosya değil (klasör olabilir) hatası.
        PermissonDenied (str): Dosya erişim yetkisi yok hatası.
    """

    FileDoesntExist = "File does not exist"
    NotFile = "is not a File"
    PermissonDenied = "Permission denied"


class File:
    """Dosya nesnesi ve validasyon işlemleri.
    
    Bu sınıf bir dosya path'ini alır, validate eder ve metadata bilgilerini
    sağlar. Dosya işlemlerinden önce mutlaka __post_init__() çağrılmalıdır.
    
    Attributes:
        path (Path): Dosyanın Path objesi.
    
    Example:
        >>> file = File("/path/to/data.csv")
        >>> file.__post_init__()  # Validate
        >>> metadata = file.get_metadata()
        >>> print(metadata['name'])
        'data.csv'
    """

    def __init__(self, path: str):
        """File sınıfını başlatır.
        
        Args:
            path (str): Dosyanın tam yolu (absolute veya relative).
        
        Note:
            Bu method sadece path'i saklar. Validasyon için mutlaka
            __post_init__() çağrılmalıdır.
        """
        self.path = Path(path)

    def __post_init__(self):
        """Dosya validasyonu yapar.
        
        Dosyanın var olup olmadığını, bir dosya olup olmadığını (klasör değil)
        ve erişim yetkisi olup olmadığını kontrol eder.
        
        Raises:
            SystemExit: Dosya bulunamadığında, klasör olduğunda veya
                erişim yetkisi olmadığında program sonlandırılır.
        
        Example:
            >>> file = File("data.csv")
            >>> file.__post_init__()  # Hata yoksa devam, varsa sys.exit()
        
        Warning:
            Bu method doğrudan sys.exit() çağırır. Hata yakalama için
            try-except kullanılması önerilmez, bunun yerine dosya yolunu
            önceden kontrol edin.
        """
        try:
            # Convert to Path object for better handling
            path = self.get_path()

            # Check if file exists
            if not path.exists():
                sys.exit(f"An Error occur: {FileError.FileDoesntExist.value}")

            # Check if it's actually a file (not a directory)
            if not path.is_file():
                sys.exit(f"An Error occur: {FileError.NotFile.value}")

        except PermissionError:
            sys.exit(f"An Error occur: {FileError.PermissonDenied.value}")
        except Exception as e:
            sys.exit(f"Unexpected Error: {str(e)}")

    def get_metadata(self) -> dict[str, str | int | float]:
        """Dosya metadata bilgilerini döndürür.
        
        Dosyanın adı, uzantısı, boyutu gibi meta bilgileri çıkarır.
        
        Returns:
            dict[str, str | int | float]: Metadata sözlüğü, aşağıdaki anahtarları içerir:
                - name (str): Dosyanın tam adı (uzantı ile birlikte).
                - stem (str): Dosya adı (uzantısız).
                - extension (str): Dosya uzantısı (örn: '.csv').
                - size_kb (float): Dosya boyutu KB cinsinden.
                - size_mb (float): Dosya boyutu MB cinsinden.
        
        Example:
            >>> file = File("data.csv")
            >>> file.__post_init__()
            >>> metadata = file.get_metadata()
            >>> print(f"File: {metadata['name']}, Size: {metadata['size_kb']} KB")
            File: data.csv, Size: 12.45 KB
        """
        path = self.get_path()

        stat = path.stat()

        metadata = {
            "name": path.name,  # Full filename
            "stem": path.stem,  # Filename without extension
            "extension": path.suffix,  # Extension (e.g., .txt)
            "size_kb": round(stat.st_size / 1024, 2),
            "size_mb": round(stat.st_size / (1024**2), 2),
        }

        return metadata

    def validate_suffix(self) -> bool:
        """Dosya uzantısının desteklenen formatlardan biri olup olmadığını kontrol eder.
        
        FileExtension enum'undaki uzantılarla karşılaştırma yapar.
        
        Returns:
            bool: Uzantı destekleniyorsa True, değilse False.
        
        Example:
            >>> file = File("data.csv")
            >>> file.__post_init__()
            >>> if file.validate_suffix():
            ...     print("Supported format")
            Supported format
        
        See Also:
            FileExtension: Desteklenen uzantılar listesi.
        """
        metadata = self.get_metadata()
        extension = metadata.get("extension")

        if extension not in {ext.value for ext in FileExtension}:
            return False

        return True

    def get_path(self) -> Path:
        """Dosyanın Path objesini döndürür.
        
        Returns:
            Path: pathlib.Path objesi.
        
        Example:
            >>> file = File("/path/to/data.csv")
            >>> path = file.get_path()
            >>> print(path.absolute())
            /absolute/path/to/data.csv
        """
        return self.path


class FileHandler:
    """Dosya okuma ve veri işleme operasyonları.
    
    Bu sınıf, File nesnelerini alır ve pandas DataFrame'e dönüştürür.
    Farklı dosya formatları (CSV, Excel, JSON, TXT) için uygun okuyucuları kullanır.
    
    Attributes:
        file (File): İşlenecek dosya nesnesi.
        data (pd.DataFrame | None): Okunan veri DataFrame'i. İlk okumadan önce None.
    
    Example:
        >>> file = File("employees.xlsx")
        >>> file.__post_init__()
        >>> handler = FileHandler(file)
        >>> data = handler.read_file()
        >>> handler.preview_data(rows=5)
    """

    def __init__(self, file: File):
        """FileHandler sınıfını başlatır.
        
        Args:
            file (File): Validate edilmiş File nesnesi.
        
        Note:
            File nesnesi üzerinde __post_init__() çağrılmış olmalıdır.
        """
        self.file = file
        self.data: pd.DataFrame | None = None

    def read_file(self) -> pd.DataFrame:
        """Dosyayı uzantısına göre okur ve DataFrame'e dönüştürür.
        
        Dosya uzantısını tespit eder ve uygun pandas okuyucusunu kullanır:
        - CSV: pd.read_csv()
        - Excel: pd.read_excel()
        - JSON: pd.read_json()
        - TXT: pd.read_csv() ile otomatik delimiter tespiti
        
        Returns:
            pd.DataFrame: Okunan veri DataFrame'i.
        
        Raises:
            SystemExit: Dosya okunamadığında veya desteklenmeyen format olduğunda.
        
        Example:
            >>> handler = FileHandler(file)
            >>> df = handler.read_file()
            >>> print(df.shape)
            (100, 5)
        
        Note:
            Bu method self.data'yı günceller, sonraki çağrılarda
            get_data() kullanılabilir.
        
        Warning:
            Excel dosyaları için openpyxl kütüphanesi yüklü olmalıdır:
            pip install openpyxl
        """
        extension = self.file.get_metadata()["extension"]
        path = self.file.get_path()

        try:
            if extension == FileExtension.CSV.value:
                self.data = pd.read_csv(path)
            elif extension in [
                FileExtension.EXCEL.value,
                FileExtension.EXCEL_OLD.value,
            ]:
                self.data = pd.read_excel(path)
            elif extension == FileExtension.JSON.value:
                self.data = pd.read_json(path)
            elif extension == FileExtension.TXT.value:
                # Otomatik delimiter tespiti için sep=None ve python engine
                self.data = pd.read_csv(path, sep=None, engine="python")
            else:
                raise ValueError(f"Unsupported file type: {extension}")

            return self.data

        except Exception as e:
            sys.exit(f"❌ Error reading file: {str(e)}")

    def get_data(self) -> pd.DataFrame | None:
        """Okunan veriyi döndürür, eğer henüz okunmadıysa okur.
        
        Lazy loading pattern kullanır. İlk çağrıda read_file() çağırır,
        sonraki çağrılarda cache'lenmiş veriyi döndürür.
        
        Returns:
            pd.DataFrame | None: Veri DataFrame'i veya henüz okunmadıysa None.
        
        Example:
            >>> handler = FileHandler(file)
            >>> data = handler.get_data()  # İlk çağrı, dosyayı okur
            >>> data2 = handler.get_data()  # İkinci çağrı, cache'den döner
        """
        if self.data is None:
            self.read_file()
        return self.data

    def get_column_names(self) -> list[str]:
        """DataFrame'in kolon isimlerini liste olarak döndürür.
        
        Returns:
            list[str]: Kolon isimleri listesi. Veri yoksa boş liste.
        
        Example:
            >>> columns = handler.get_column_names()
            >>> print(columns)
            ['Name', 'Age', 'City', 'Salary']
        """
        if self.data is None:
            return []
        return self.data.columns.tolist()

    def preview_data(self, rows: int = 5):
        """Verinin önizlemesini konsola yazdırır.
        
        İlk N satırı, DataFrame boyutunu ve kolon isimlerini gösterir.
        
        Args:
            rows (int, optional): Görüntülenecek satır sayısı. Varsayılan 5.
        
        Example:
            >>> handler.preview_data(rows=10)
            📊 Data Preview (first 10 rows):
            ...
            📈 Shape: 100 rows × 5 columns
            📋 Columns: Name, Age, City, Salary, Department
        
        Note:
            Veri henüz okunmadıysa hiçbir şey yapmaz (None döner).
        """
        if self.data is None:
            return

        print(f"\n📊 Data Preview (first {rows} rows):")
        print(self.data.head(rows).to_string())
        print(f"\n📈 Shape: {self.data.shape[0]} rows × {self.data.shape[1]} columns")
        print(f"📋 Columns: {', '.join(self.get_column_names())}")
