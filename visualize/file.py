import sys
from enum import Enum
from pathlib import Path

import pandas as pd


class FileExtension(Enum):
    "Common file types for data analysis"

    "NOTE: this enum is a project specific its not comprehensive enough"

    CSV = ".csv"
    EXCEL = ".xlsx"
    EXCEL_OLD = ".xls"
    JSON = ".json"
    TXT = ".txt"


class FileError(Enum):
    FileDoesntExist = "File does not exist"
    NotFile = "is not a File"
    PermissonDenied = "Permission denied"


class File:
    def __init__(self, path: str):
        self.path = Path(path)

    def __post_init__(self):
        """
        Validation for given file
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
        metadata = self.get_metadata()
        extension = metadata.get("extension")

        if extension not in {ext.value for ext in FileExtension}:
            return False

        return True

    def get_path(self) -> Path:
        return self.path


class FileHandler:
    """Handles file reading operations"""

    def __init__(self, file: File):
        self.file = file
        self.data: pd.DataFrame | None = None

    def read_file(self) -> pd.DataFrame:
        """Read file based on extension"""
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
                self.data = pd.read_csv(path, sep=None, engine="python")
            else:
                raise ValueError(f"Unsupported file type: {extension}")

            return self.data

        except Exception as e:
            sys.exit(f"❌ Error reading file: {str(e)}")

    def get_data(self) -> pd.DataFrame | None:
        if self.data is None:
            self.read_file()
        return self.data

    def get_column_names(self) -> list[str]:
        if self.data is None:
            return []
        return self.data.columns.tolist()

    def preview_data(self, rows: int = 5):
        """Show preview of data"""
        if self.data is None:
            return

        print(f"\n📊 Data Preview (first {rows} rows):")
        print(self.data.head(rows).to_string())
        print(f"\n📈 Shape: {self.data.shape[0]} rows × {self.data.shape[1]} columns")
        print(f"📋 Columns: {', '.join(self.get_column_names())}")
