from pathlib import Path

from parsers.taxonomies_parser import TaxonomyParser

MODULES_FOLDER = Path(__file__).parent / "modules"
INDEX_PATH = MODULES_FOLDER / "index.json"
DIM_DOM_MAPPING_PATH = MODULES_FOLDER / "dim_dom_mapping.json"


class TaxonomyLoaderServiceHandler:

    @staticmethod
    def load(input_path: str | Path) -> None:
        input_path = input_path if isinstance(input_path, Path) else Path(input_path)
        # file exists?
        if not input_path.exists():
            raise FileNotFoundError(f"File {input_path} not found")
        # file is compress??
        if input_path.suffix not in [".zip", ".7z"]:
            raise ValueError("Input file must be a zip or 7z file")
        # parse tax
        TaxonomyParser.from_json(input_path)
        # serialize to file
