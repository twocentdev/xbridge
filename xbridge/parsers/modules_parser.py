import json
from pathlib import Path
from time import time
from zipfile import ZipFile
from lxml import etree

from builders.module_builder import ModuleBuilder
from models.module import Module


MODULES_FOLDER = Path(__file__).parent / "modules"
INDEX_PATH = MODULES_FOLDER / "index.json"
DIM_DOM_MAPPING_PATH = MODULES_FOLDER / "dim_dom_mapping.json"


class ModulesParser:

    @staticmethod
    def from_json(input_path: Path = None):
        """loads the modules in the taxonomy"""
        modules: [Module] = []

        with ZipFile(input_path, mode="r") as zip_file:
            for file_path in zip_file.namelist():
                file_path_obj = Path(file_path)
                if (
                        file_path_obj.suffix == ".json"
                        and file_path_obj.parent.name == "mod"
                        and not str(file_path_obj).startswith("__MACOSX")  # avoid processing internal macOS files
                        and not str(file_path_obj).endswith(".DS_Store")
                ):
                    mod_builder = ModuleBuilder()
                    mod_builder.set_code(file_path_obj.stem)
                    mod_builder.set_url(file_path)
                    mod_builder.set_taxonomy_code(file_path.split("/")[7])
                    mod_builder.set_date(file_path.split("/")[8])
                    mod_builder.set_taxonomy_module_path(file_path)
                    modules.append(mod_builder.build())
        if not modules:
            raise TypeError(
                (
                    "No modules found in the taxonomy. "
                    "Please check that the zip file does not contain "
                    "zip files within it"
                )
            )
        return modules
    