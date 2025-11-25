from dataclasses import dataclass
from enum import Enum

class FileExtension(Enum)
    "Common file types for data analysis"
    "NOTE: this enum is a project specific its not comprehensive enough"

    CSV = ".csv"
    EXCEL = ".xlsx"
    EXCEL_OLD = ".xls"
    JSON = ".json"
    TXT = ".txt"

@dataclass
class FileInterface:
    "File interface"

    name: str
    file_extension: FileExtension

    def __post_init__(self):
        "TODO: seek file for metadata"
        pass

    def metadata(self):
        "TODO: remove the print function to avoid side-effects"
        pass
