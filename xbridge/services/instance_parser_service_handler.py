from pathlib import Path

from parsers.instance_parser import InstanceParser
from serializers.instance_serializer import InstanceSerializer


class InstanceParserServiceHandler:

    @staticmethod
    def parse(input_path: str | Path, modules_path: str | Path, output_path: str | Path):
        input_path = input_path if isinstance(input_path, Path) else Path(input_path)
        modules_path = modules_path if isinstance(modules_path, Path) else Path(modules_path)
        output_path = output_path if isinstance(output_path, Path) else Path(output_path)

        if not input_path.exists():
            raise FileNotFoundError(f"File {input_path} not found")
        if not modules_path.exists():
            raise FileNotFoundError(f"Modules not found")
        if not (modules_path / "index.json").exists():
            raise FileNotFoundError(f"Modules index not found")
        # if output_path.exists()

        # Parse instance file
        instance = InstanceParser.from_xml(input_path)
        print(instance)
        # Transform into CSV
        # Save file
        InstanceSerializer.to_csv_dpm_1_0(output_path, modules_path, instance)
