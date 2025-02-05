import json
from pathlib import Path

from models.dim_dom_map import DimDomMap


class DimDomMapSerializer:

    @staticmethod
    def to_json(output_path: Path, map_: DimDomMap):
        if not output_path.exists():
            output_path.mkdir()
        with open(output_path / "dim_dom_mapping.json",
                  mode="w",
                  encoding="utf-8") as file:
            json.dump(map_.map, file, indent=4)
