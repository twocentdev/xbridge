import json
from pathlib import Path


class ModulesIndexSerializer:

    @staticmethod
    def to_json(output_path: Path, map_: dict):
        if not output_path.exists():
            output_path.mkdir()
        with open(output_path / "index.json",
                  mode="w",
                  encoding="UTF-8") as file:
            json.dump(map_, file, indent=4)
