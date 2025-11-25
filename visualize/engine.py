import sys

from file import File, FileHandler

from visualize import VisualizationHandler


class VisiualEngine:
    """Brings together everything"""

    def __init__(self):
        self.file: File | None = None
        self.file_handler: FileHandler | None = None
        self.viz_handler: VisualizationHandler | None = None
        self.project_link: str = "https://www.github.com/riqoto/visual"

    def setup_file(self, file_path: str):
        """Setup file and file handler"""
        self.file = File(file_path)
        self.file.__post_init__()  # Call validation

        if not self.file.validate_suffix():
            sys.exit("❌ Unsupported file type")

        # Show file metadata
        metadata = self.file.get_metadata()
        print(f"\n📄 File Info:")
        print(f"   Name: {metadata['name']}")
        print(f"   Size: {metadata['size_kb']} KB")
        print(f"   Type: {metadata['extension']}")

        self.file_handler = FileHandler(self.file)
        self.file_handler.read_file()

    def setup_visualization(self):
        """Setup visualization handler"""
        if self.file_handler is None:
            print("❌ File handler not initialized")
            return

        self.viz_handler = VisualizationHandler(self.file_handler)
        self.viz_handler.interactive_visualization()

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

    def run(self, file_path: str):
        """Complete workflow for single file"""
        self.intro()

        self.setup_file(file_path)
        self.setup_visualization()

        print("\n✅ Workflow completed!")

    def run_multiple(self, file_paths: list[str]):
        """Complete workflow for multiple files"""
        print("\n" + "=" * 50)
        print("🎨 VISUALIZATION WORKFLOW - MULTIPLE FILES")
        print("=" * 50)

        for i, file_path in enumerate(file_paths, 1):
            print(f"\n{'=' * 50}")
            print(f"📁 Processing File {i}/{len(file_paths)}")
            print(f"{'=' * 50}")

            try:
                self.setup_file(file_path)
                self.setup_visualization()
            except KeyboardInterrupt:
                print("\n\n👋 Exiting...")
                break
            except Exception as e:
                print(f"❌ Error processing {file_path}: {str(e)}")
                continue

        print("\n✅ All files processed!")
