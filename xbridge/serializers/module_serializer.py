import json
from pathlib import Path

from models.module import Module


class ModuleSerializer:

    @staticmethod
    def to_json(output_path: Path, module: Module):
        if not output_path.exists():
            output_path.mkdir()
        with open(output_path / module.file_name,
                  mode="w",
                  encoding="utf-8") as file:
            json.dump(module.to_dict(), file, indent=4)
