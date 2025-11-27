"""Görselleştirme motoru ve stratejileri modülü.

Bu modül, verilerin görselleştirilmesi için gerekli olan tüm mantığı,
stratejileri ve workflow yönetimini içerir. Strategy pattern kullanılarak
farklı grafik türleri (Line, Bar, Histogram, Table) implement edilmiştir.

Classes:
    VisualizationType: Desteklenen grafik türleri enum'u.
    VisualizationStrategy: Grafik stratejileri için abstract base class.
    LineChartStrategy: Çizgi grafiği oluşturma stratejisi.
    BarChartStrategy: Çubuk grafiği oluşturma stratejisi.
    HistogramStrategy: Histogram oluşturma stratejisi.
    TableStrategy: Tablo görünümü oluşturma stratejisi.
    VisualizationHandler: Görselleştirme işlemlerini yöneten handler.
    VisualizationWorkflow: Tüm görselleştirme akışını yöneten orchestrator.

Example:
    Temel kullanım::

        from visualize import VisualizationWorkflow
        
        workflow = VisualizationWorkflow()
        workflow.run("data.csv")
"""

import sys
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from file import File, FileHandler
from InquirerPy import inquirer

# GUI Backend ayarları
try:
    matplotlib.use("TkAgg")  # Try TkAgg first (most common)
except ImportError:
    try:
        matplotlib.use("Qt5Agg")  # Try Qt5Agg
    except ImportError:
        try:
            matplotlib.use("GTK3Agg")  # Try GTK3Agg
        except ImportError:
            print("⚠️  Warning: No GUI backend found. Using default backend.")
            print("   Install one of: python3-tk, PyQt5, or PyGObject")
            matplotlib.use("Agg")
            sys.exit()


class VisualizationType(Enum):
    """Desteklenen görselleştirme türleri.
    
    Attributes:
        LINE_CHART (str): Çizgi grafiği.
        BAR_CHART (str): Çubuk grafiği.
        HISTOGRAM (str): Histogram.
        TABLE (str): Veri tablosu.
    """

    LINE_CHART = "Line Chart"
    BAR_CHART = "Bar Chart"
    HISTOGRAM = "Histogram"
    TABLE = "Table"


class VisualizationStrategy(ABC):
    """Görselleştirme stratejileri için soyut temel sınıf (Abstract Base Class).
    
    Tüm grafik stratejileri bu sınıftan türetilmeli ve create_visualization
    methodunu implement etmelidir.
    """

    @abstractmethod
    def create_visualization(self, data: pd.DataFrame, config: dict):
        """Spesifik bir grafik türü oluşturur.
        
        Args:
            data (pd.DataFrame): Görselleştirilecek veri.
            config (dict): Grafik konfigürasyonu (başlık, eksenler vb.).
        
        Raises:
            NotImplementedError: Alt sınıflar bu methodu implement etmelidir.
        """
        pass


class LineChartStrategy(VisualizationStrategy):
    """Çizgi grafiği (Line Chart) oluşturma stratejisi."""

    def create_visualization(self, data: pd.DataFrame, config: dict):
        """Verilen veri ve konfigürasyon ile çizgi grafiği oluşturur.
        
        Args:
            data (pd.DataFrame): Görselleştirilecek veri.
            config (dict): Konfigürasyon sözlüğü.
                - x_axis (str): X ekseni kolon adı.
                - y_axis (str): Y ekseni kolon adı.
                - title (str, optional): Grafik başlığı.
        
        Example:
            >>> strategy = LineChartStrategy()
            >>> config = {'x_axis': 'Date', 'y_axis': 'Sales', 'title': 'Sales Trend'}
            >>> strategy.create_visualization(df, config)
        """
        print("📈 Creating Line Chart...")

        x_col = config.get("x_axis")
        y_col = config.get("y_axis")
        title = config.get("title", "Line Chart")

        plt.figure(figsize=(10, 6))
        plt.plot(
            data[x_col],
            data[y_col],
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=6,
        )
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title, fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        # Check if we can show interactive plot
        if matplotlib.get_backend() != "Agg":
            plt.show()
        else:
            # Save to file if no GUI available
            filename = f"line_chart_{x_col}_{y_col}.png"
            plt.savefig(filename, dpi=150, bbox_inches="tight")
            print(f"✅ Line Chart saved as: {filename}")
            plt.close()

        print("✅ Line Chart created successfully!")


class BarChartStrategy(VisualizationStrategy):
    """Çubuk grafiği (Bar Chart) oluşturma stratejisi."""

    def create_visualization(self, data: pd.DataFrame, config: dict):
        """Verilen veri ve konfigürasyon ile çubuk grafiği oluşturur.
        
        Args:
            data (pd.DataFrame): Görselleştirilecek veri.
            config (dict): Konfigürasyon sözlüğü.
                - x_axis (str): Kategorik eksen (X).
                - y_axis (str): Değer ekseni (Y).
                - title (str, optional): Grafik başlığı.
        """
        print("📊 Creating Bar Chart...")

        x_col = config.get("x_axis")
        y_col = config.get("y_axis")
        title = config.get("title", "Bar Chart")

        plt.figure(figsize=(10, 6))
        plt.bar(data[x_col], data[y_col], color="steelblue", alpha=0.8)
        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(title, fontsize=14, fontweight="bold")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()

        if matplotlib.get_backend() != "Agg":
            plt.show()
        else:
            filename = f"bar_chart_{x_col}_{y_col}.png"
            plt.savefig(filename, dpi=150, bbox_inches="tight")
            print(f"✅ Bar Chart saved as: {filename}")
            plt.close()

        print("✅ Bar Chart created successfully!")


class HistogramStrategy(VisualizationStrategy):
    """Histogram oluşturma stratejisi."""

    def create_visualization(self, data: pd.DataFrame, config: dict):
        """Verilen veri ve konfigürasyon ile histogram oluşturur.
        
        Args:
            data (pd.DataFrame): Görselleştirilecek veri.
            config (dict): Konfigürasyon sözlüğü.
                - column (str): Analiz edilecek kolon.
                - bins (int, optional): Bin sayısı. Varsayılan 30.
                - title (str, optional): Grafik başlığı.
        """
        print("📊 Creating Histogram...")

        column = config.get("column")
        title = config.get("title", f"Histogram of {column}")
        bins = config.get("bins", 30)

        plt.figure(figsize=(10, 6))
        plt.hist(
            data[column].dropna(), bins=bins, color="teal", alpha=0.7, edgecolor="black"
        )
        plt.xlabel(column, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.title(title, fontsize=14, fontweight="bold")
        plt.grid(True, alpha=0.3, axis="y")
        plt.tight_layout()

        if matplotlib.get_backend() != "Agg":
            plt.show()
        else:
            filename = f"histogram_{column}.png"
            plt.savefig(filename, dpi=150, bbox_inches="tight")
            print(f"✅ Histogram saved as: {filename}")
            plt.close()

        print("✅ Histogram created successfully!")


class TableStrategy(VisualizationStrategy):
    """Tablo görünümü oluşturma stratejisi."""

    def create_visualization(self, data: pd.DataFrame, config: dict):
        """Veriyi matplotlib tablosu olarak görselleştirir.
        
        Args:
            data (pd.DataFrame): Görselleştirilecek veri.
            config (dict): Konfigürasyon sözlüğü.
                - rows (int, optional): Gösterilecek satır sayısı. Varsayılan 10.
                - title (str, optional): Tablo başlığı.
        """
        print("📋 Creating Table...")

        title = config.get("title", "Data Table")
        rows = config.get("rows", 10)

        display_data = data.head(rows)

        fig, ax = plt.subplots(figsize=(14, max(4, rows * 0.4)))
        ax.axis("tight")
        ax.axis("off")

        table = ax.table(
            cellText=display_data.values,
            colLabels=display_data.columns,
            cellLoc="center",
            loc="center",
            colColours=["#4472C4"] * len(display_data.columns),
        )

        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1, 2)

        # Style header
        for i in range(len(display_data.columns)):
            table[(0, i)].set_facecolor("#4472C4")
            table[(0, i)].set_text_props(weight="bold", color="white")

        plt.title(title, fontsize=14, fontweight="bold", pad=20)
        plt.tight_layout()

        if matplotlib.get_backend() != "Agg":
            plt.show()
        else:
            filename = f"table_{title.replace(' ', '_')}.png"
            plt.savefig(filename, dpi=150, bbox_inches="tight")
            print(f"✅ Table saved as: {filename}")
            plt.close()

        print("✅ Table created successfully!")


class VisualizationHandler:
    """Görselleştirme işlemlerini yöneten handler sınıfı.
    
    Strateji seçimi, konfigürasyon yönetimi ve kullanıcı etkileşimi
    (prompt'lar) bu sınıf üzerinden yürütülür.
    
    Attributes:
        file_handler (FileHandler): Veri kaynağı handler'ı.
        strategy (VisualizationStrategy | None): Seçili görselleştirme stratejisi.
        config (dict): Görselleştirme konfigürasyonu.
        strategies (dict): Mevcut stratejilerin haritası.
    """

    def __init__(self, file_handler: FileHandler):
        """VisualizationHandler'ı başlatır.
        
        Args:
            file_handler (FileHandler): Veri kaynağı.
        """
        self.file_handler = file_handler
        self.strategy: VisualizationStrategy | None = None
        self.config: dict = {}
        self.strategies = {
            VisualizationType.LINE_CHART: LineChartStrategy(),
            VisualizationType.BAR_CHART: BarChartStrategy(),
            # VisualizationType.HISTOGRAM: HistogramStrategy(),
            VisualizationType.TABLE: TableStrategy(),
        }

    def set_strategy(self, viz_type: VisualizationType):
        """Görselleştirme tipine göre stratejiyi ayarlar.
        
        Args:
            viz_type (VisualizationType): İstenen grafik türü.
        """
        self.strategy = self.strategies.get(viz_type)
        if self.strategy is None:
            print(f"⚠️  Visualization type {viz_type.value} not implemented yet")

    def configure(self, **kwargs):
        """Görselleştirme parametrelerini günceller.
        
        Args:
            **kwargs: Konfigürasyon parametreleri (x_axis, title vb.).
        """
        self.config.update(kwargs)
        print(f"⚙️  Configuration updated: {self.config}")

    def create_visualization(self):
        """Mevcut strateji ve konfigürasyon ile görselleştirmeyi oluşturur.
        
        Veriyi FileHandler'dan alır ve stratejinin create_visualization
        methodunu çağırır.
        
        Note:
            Strateji veya veri yoksa hata mesajı yazdırır.
        """
        if self.strategy is None:
            print("❌ No visualization strategy set")
            return

        data = self.file_handler.get_data()
        if data is None:
            print("❌ No data available for visualization")
            return

        try:
            self.strategy.create_visualization(data, self.config)
        except Exception as e:
            print(f"❌ Error creating visualization: {str(e)}")

    def prompt_visualization_type(self) -> VisualizationType | None:
        """Kullanıcıdan görselleştirme türünü seçmesini ister.
        
        Returns:
            VisualizationType | None: Seçilen tür veya iptal durumunda None.
        """
        try:
            viz_types = list(VisualizationType)
            choices = [viz_type.value for viz_type in viz_types]

            selected = inquirer.select(
                message="Select Visualization Type:",
                choices=choices,
                default=choices[0],
                border=True,
                qmark="🎨",
                keybindings={
                    "interrupt": [{"key": "q"}],
                },
            ).execute()

            # Find the enum member by value
            for viz_type in viz_types:
                if viz_type.value == selected:
                    print(f"✅ Selected: {selected}")
                    return viz_type

            return None

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            return None
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            return None

    def prompt_configuration(self, viz_type: VisualizationType) -> dict:
        """Seçilen grafik türüne göre kullanıcıdan konfigürasyon alır.
        
        Grafik türüne göre farklı sorular sorar (X ekseni, Y ekseni, başlık vb.).
        
        Args:
            viz_type (VisualizationType): Seçilen grafik türü.
        
        Returns:
            dict: Oluşturulan konfigürasyon sözlüğü.
        """
        columns = self.file_handler.get_column_names()

        try:
            config = {}

            if viz_type == VisualizationType.HISTOGRAM:
                """Fix the weird look issue"""
                pass
                # print("\n⚙️  Histogram Configuration:")

                # # Column selection
                # col = inquirer.select(
                #     message="Select column to analyze:",
                #     choices=columns,
                #     default=columns[0],
                #     border=True,
                #     qmark="📊",
                #     keybindings={"interrupt": [{"key": "q"}]},
                # ).execute()

                # # Bins
                # bins = inquirer.text(
                #     message="Number of bins:",
                #     default="30",
                #     validate=lambda x: x.isdigit() and int(x) > 0,
                #     invalid_message="Please enter a positive number",
                #     qmark="🔢",
                # ).execute()

                # # Title
                # title = inquirer.text(
                #     message="Chart title:",
                #     default=f"Histogram of {col}",
                #     qmark="📝",
                # ).execute()

                # config = {"column": col, "bins": int(bins), "title": title}

            elif viz_type == VisualizationType.TABLE:
                print("\n⚙️  Table Configuration:")

                rows = inquirer.text(
                    message="Number of rows to display:",
                    default="10",
                    validate=lambda x: x.isdigit() and int(x) > 0,
                    invalid_message="Please enter a positive number",
                    qmark="🔢",
                    keybindings={"interrupt": [{"key": "q"}]},
                ).execute()

                title = inquirer.text(
                    message="Table title:",
                    default="Data Table",
                    qmark="📝",
                    keybindings={"interrupt": [{"key": "q"}]},
                ).execute()

                config = {"rows": int(rows), "title": title}

            else:  # Line Chart or Bar Chart
                print(f"\n⚙️  {viz_type.value} Configuration:")

                # X-axis
                x_col = inquirer.select(
                    message="Select X-axis column:",
                    choices=columns,
                    default=columns[0],
                    border=True,
                    qmark="📈",
                    keybindings={"interrupt": [{"key": "q"}]},
                ).execute()

                # Y-axis
                y_col = inquirer.select(
                    message="Select Y-axis column:",
                    choices=columns,
                    default=columns[1] if len(columns) > 1 else columns[0],
                    border=True,
                    qmark="📊",
                    keybindings={"interrupt": [{"key": "q"}]},
                ).execute()

                # Title
                title = inquirer.text(
                    message="Chart title:",
                    default=viz_type.value,
                    qmark="📝",
                    keybindings={"interrupt": [{"key": "q"}]},
                ).execute()

                config = {"x_axis": x_col, "y_axis": y_col, "title": title}

            self.configure(**config)
            return config

        except KeyboardInterrupt:
            print("\n👋 Exiting configuration...")
            return {}

    def interactive_visualization(self):
        """Tam interaktif görselleştirme akışını başlatır.
        
        1. Veri önizlemesi gösterir.
        2. Döngü içinde kullanıcıdan grafik türü ve konfigürasyon alır.
        3. Grafiği oluşturur.
        4. Başka grafik isteyip istemediğini sorar.
        """
        self.file_handler.preview_data()

        while True:
            viz_type = self.prompt_visualization_type()
            if viz_type is None:
                break

            self.set_strategy(viz_type)

            config = self.prompt_configuration(viz_type)
            if not config:
                break

            self.create_visualization()

            try:
                another = inquirer.confirm(
                    message="Create another visualization for this file?",
                    default=False,
                    qmark="🔄",
                    keybindings={"interrupt": [{"key": "q"}]},
                ).execute()

                if not another:
                    break

            except KeyboardInterrupt:
                print("\n\n👋 Exiting visualization...")
                break


class VisualizationWorkflow:
    """Tüm görselleştirme iş akışını yöneten orchestrator sınıfı.
    
    Dosya hazırlığı, handler kurulumu ve farklı çalışma modlarını (tek dosya,
    çoklu dosya, karşılaştırma) yönetir.
    
    Attributes:
        file (File | None): Aktif dosya nesnesi.
        file_handler (FileHandler | None): Aktif dosya handler'ı.
        viz_handler (VisualizationHandler | None): Aktif görselleştirme handler'ı.
    """

    def __init__(self):
        """VisualizationWorkflow sınıfını başlatır."""
        self.file: File | None = None
        self.file_handler: FileHandler | None = None
        self.viz_handler: VisualizationHandler | None = None

    def setup_file(self, file_path: str):
        """Dosyayı ve file handler'ı hazırlar.
        
        Args:
            file_path (str): Dosya yolu.
        
        Raises:
            SystemExit: Dosya tipi desteklenmiyorsa.
        """
        self.file = File(file_path)
        self.file.__post_init__()  # Call validation

        if not self.file.validate_suffix():
            sys.exit("❌ Unsupported file type")

        metadata = self.file.get_metadata()
        print(f"\n📄 File Info:")
        print(f"   Name: {metadata['name']}")
        print(f"   Size: {metadata['size_kb']} KB")
        print(f"   Type: {metadata['extension']}")

        self.file_handler = FileHandler(self.file)
        self.file_handler.read_file()

    def setup_visualization(self):
        """Visualization handler'ı kurar ve interaktif akışı başlatır."""
        if self.file_handler is None:
            print("❌ File handler not initialized")
            return

        self.viz_handler = VisualizationHandler(self.file_handler)
        self.viz_handler.interactive_visualization()

    def run(self, file_path: str):
        """Tek bir dosya için workflow'u çalıştırır.
        
        Args:
            file_path (str): Dosya yolu.
        """
        print("\n" + "=" * 50)
        print("🎨 VISUALIZATION WORKFLOW")
        print("=" * 50)

        self.setup_file(file_path)
        self.setup_visualization()

        print("\n✅ Workflow completed!")

    def run_with_shared_config(self, file_paths: list[str]):
        """Birden fazla dosya için akıllı workflow'u çalıştırır.
        
        Kullanıcıya çalışma modu seçtirir:
        1. Tüm dosyalar için aynı görselleştirme
        2. Her dosya için farklı görselleştirme
        3. Dosyaları karşılaştırma
        
        Args:
            file_paths (list[str]): Dosya yolları listesi.
        """
        print("\n" + "=" * 50)
        print(f"🎨 SMART VISUALIZATION WORKFLOW - {len(file_paths)} FILES")
        print("=" * 50)

        from InquirerPy import inquirer

        mode = inquirer.select(
            message="How do you want to visualize these files?",
            choices=[
                "🔄 Same visualization for all files (recommended)",
                "📊 Different visualization for each file",
                "🎯 Compare files side-by-side",
            ],
            default="🔄 Same visualization for all files (recommended)",
            qmark="🤔",
            keybindings={"interrupt": [{"key": "q"}]},
        ).execute()

        if "Same visualization" in mode:
            self._run_same_visualization_for_all(file_paths)
        elif "Different visualization" in mode:
            self._run_different_visualization_for_each(file_paths)
        else:  # Compare files
            self._run_comparison(file_paths)

        print("\n✅ All files processed!")

    def _run_same_visualization_for_all(self, file_paths: list[str]):
        """Tüm dosyalar için aynı görselleştirme tipini uygular.
        
        Önce tüm dosyaları yükler, sonra kullanıcıdan bir kez konfigürasyon alır
        ve bu konfigürasyonu tüm dosyalara uygular.
        
        Args:
            file_paths (list[str]): Dosya yolları listesi.
        """
        print("\n📋 Loading all files...")

        file_handlers = []
        for file_path in file_paths:
            try:
                file = File(file_path)
                file.__post_init__()
                fh = FileHandler(file)
                fh.read_file()
                file_handlers.append((file_path, fh))
                print(f"  ✅ Loaded: {file.get_metadata()['name']}")
            except Exception as e:
                print(f"  ❌ Failed to load {file_path}: {str(e)}")

        if not file_handlers:
            print("❌ No files loaded successfully")
            return

        _, first_handler = file_handlers[0]

        viz_handler = VisualizationHandler(first_handler)

        # Kullanıcıdan visualization tipi al
        print("\n📊 All files will use the SAME visualization type and configuration")
        viz_type = viz_handler.prompt_visualization_type()
        if viz_type is None:
            return

        viz_handler.set_strategy(viz_type)

        config = viz_handler.prompt_configuration(viz_type)
        if not config:
            return

        print(f"\n🚀 Creating {viz_type.value} for all {len(file_handlers)} files...\n")

        for i, (file_path, fh) in enumerate(file_handlers, 1):
            print(f"\n{'=' * 50}")
            print(f"📄 File {i}/{len(file_handlers)}: {Path(file_path).name}")
            print(f"{'=' * 50}")

            # Her dosya için yeni handler oluştur ama aynı config kullan
            temp_viz_handler = VisualizationHandler(fh)
            temp_viz_handler.set_strategy(viz_type)
            temp_viz_handler.config = config.copy()
            temp_viz_handler.create_visualization()

    def _run_different_visualization_for_each(self, file_paths: list[str]):
        """Her dosya için ayrı ayrı görselleştirme akışı çalıştırır.
        
        Args:
            file_paths (list[str]): Dosya yolları listesi.
        """
        print("\n📋 Each file will have its own visualization configuration\n")

        for i, file_path in enumerate(file_paths, 1):
            print(f"\n{'=' * 50}")
            print(f"📄 File {i}/{len(file_paths)}")
            print(f"{'=' * 50}")

            try:
                self.setup_file(file_path)
                self.setup_visualization()
            except KeyboardInterrupt:
                print("\n\n👋 Skipping remaining files...")
                break
            except Exception as e:
                print(f"❌ Error processing {file_path}: {str(e)}")
                continue

    def _run_comparison(self, file_paths: list[str]):
        """Dosyaları yan yana karşılaştırmalı olarak görselleştirir.
        
        Ortak kolonları bulur ve seçilen kolon üzerinden karşılaştırma grafiği çizer.
        
        Args:
            file_paths (list[str]): Dosya yolları listesi.
        """
        print("\n📊 Comparison mode: All files in one visualization")

        from InquirerPy import inquirer

        all_data = []
        for file_path in file_paths:
            try:
                file = File(file_path)
                file.__post_init__()
                fh = FileHandler(file)
                data = fh.read_file()
                all_data.append(
                    {"name": file.get_metadata()["name"], "data": data, "handler": fh}
                )
                print(f"  ✅ Loaded: {file.get_metadata()['name']}")
            except Exception as e:
                print(f"  ❌ Failed: {file_path}")

        if len(all_data) < 2:
            print("❌ Need at least 2 files for comparison")
            return

        common_columns = set(all_data[0]["data"].columns)
        for item in all_data[1:]:
            common_columns &= set(item["data"].columns)

        if not common_columns:
            print("❌ No common columns found across all files")
            return

        common_columns = sorted(list(common_columns))
        print(f"\n📋 Common columns: {', '.join(common_columns)}")

        viz_types = [VisualizationType.LINE_CHART, VisualizationType.BAR_CHART]
        choices = [vt.value for vt in viz_types]

        selected = inquirer.select(
            message="Select comparison chart type:",
            choices=choices,
            qmark="🎨",
            keybindings={"interrupt": [{"key": "q"}]},
        ).execute()

        x_col = inquirer.select(
            message="X-axis:",
            choices=common_columns,
            qmark="📈",
            keybindings={"interrupt": [{"key": "q"}]},
        ).execute()

        y_col = inquirer.select(
            message="Y-axis to compare:",
            choices=common_columns,
            qmark="📊",
            keybindings={"interrupt": [{"key": "q"}]},
        ).execute()

        print(f"\n🚀 Creating comparison {selected}...")

        plt.figure(figsize=(12, 7))

        for item in all_data:
            data = item["data"]
            if x_col in data.columns and y_col in data.columns:
                if "Line" in selected:
                    plt.plot(
                        data[x_col],
                        data[y_col],
                        marker="o",
                        label=item["name"],
                        linewidth=2,
                    )
                else:
                    # Bar chart için offset gerekir
                    pass  # Şimdilik sadece line chart

        plt.xlabel(x_col, fontsize=12)
        plt.ylabel(y_col, fontsize=12)
        plt.title(f"Comparison: {y_col} across files", fontsize=14, fontweight="bold")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        if matplotlib.get_backend() != "Agg":
            plt.show()
        else:
            filename = f"comparison_{y_col}.png"
            plt.savefig(filename, dpi=150, bbox_inches="tight")
            print(f"✅ Comparison saved as: {filename}")
            plt.close()

        print("✅ Comparison chart created!")
