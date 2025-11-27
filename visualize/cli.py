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
    "CLI Config interface"

    "default path for data is /data folder on current path"
    "TODO: get current path with getcwd()"
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
    FolderIsEmpty = "folder does not include any file"
    FileIsNotValid = "file is not valid"
    FolderDoesntHaveValidFileTypes = (
        "Folder do not include valid file types for visualize"
    )


class CLI(CLIConfig):
    def __init__(self, config: CLIConfig):
        self.config = config
        self.project_link: str = "https://www.github.com/riqoto/visual"

    def create_files_prompt(self):
        """Let user select file(s) from the directory"""
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

        "we already have invalid keyword and validation on select menu so we dont need to check for files len"
        "user either exit the program or select at least one file"
        return files

    def get_files(self) -> list[str]:
        """Get all files from the configured path"""
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
        print(f"📁 Scanning directory: {self.config.path}")
        print(f"Actions:\n{actions:^50}")

    """TODO: all logic works here seperate the logic
    """

    def visualize_files(self, file_names: list[str]):
        """Handle visualization for selected files"""
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
        """Run the CLI application"""
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
            print("\n⚠️  No file selected. Exiting...\n")
