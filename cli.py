import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from random import choices

from InquirerPy import inquirer


@dataclass
class CLIConfig:
    "CLI Config interface"

    "default path for data is /data folder on current path"
    path: str = "./data"
    "if given path has own other folders(childs) program needs to walk on them but right now its not possible"
    "TODO: create a Tree for walking on a path safely"
    recursive: bool = False
    "max file size for listing"
    max_file: int = 100

    def __post_init__(self):
        if not os.path.exists(self.path):
            sys.exit(f"An Error occur: {self.path} {CLIError.PathDoesntExist.value}")


class CLIError(Enum):
    DataNotFound = "data not found"
    PathDoesntExist = "path does not exist"
    FolderIsEmpty = "folder is do not include any file"


class CLI(CLIConfig):
    def __init__(self, config: CLIConfig):
        self.config = config
        self.project_link: str = "https://www.github.com/riqoto/visual"

    def create_files_prompt(self):
        files = []
        try:
            files = inquirer.checkbox(
                message="Select file/files to visiualize [press space for selection]",
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
        except:
            sys.exit("Unkown Error")

        "we already have invalid keywork and validation on select menu so we dont need to check for files len"
        "user either exit the program or select at least one file"
        return files

    def get_files(self) -> list[str]:
        files_list: list[str] = os.listdir(self.path)
        if len(files_list) == 0:
            sys.exit(f"An eror occur: {self.path} {CLIError.FolderIsEmpty.value}")
        return files_list

    def intro(self):
        """Display ASCII banner"""
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
        print(f"Actions:\n{actions:^50}")

    def run(self):
        """Run the CLI application"""
        self.intro()

        selected_file = self.create_files_prompt()

        if selected_file:
            print(f"\n✅ Selected file: {selected_file}")
            print("🚀 Starting visualization...\n")
            # Burada visualization logic'inizi ekleyin
        else:
            print("\n⚠️  No file selected. Exiting...\n")
