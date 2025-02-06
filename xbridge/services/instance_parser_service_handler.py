from pathlib import Path

from parsers.instance_parser import InstanceParser


class InstanceParserServiceHandler:

    @staticmethod
    def parse(input_path: str | Path, output_path: str | Path):
        input_path = input_path if isinstance(input_path, Path) \
            else Path(input_path)
        output_path = output_path if isinstance(output_path, Path) \
            else Path(output_path)

        if not input_path.exists():
            raise FileNotFoundError(f"File {input_path} not found")
        # if output_path.exists()

        # Parse instance file
        InstanceParser.from_xml(input_path)
        # Transform into CSV
        # Save file
