import json
import logging
from pathlib import Path
from zipfile import ZipFile

from builders.module_builder import ModuleBuilder
from parsers.tables_parser import TablesParser


logger = logging.getLogger(__name__)


class ModulesParser:

    @staticmethod
    def file_is_mod(file_path: str) -> bool:
        return (
                not file_path.startswith("__MACOSX")
                and not ".DS_Store" in file_path
                and "/mod/" in file_path
                and file_path.endswith(".json")
        )

    @staticmethod
    def filter_files(files: [str], filters: [str]) -> [str]:
        mod_files = filter(ModulesParser.file_is_mod, files)
        if len(filters) > 0:
            mod_files = filter(
                lambda x: any(x.startswith(base) for base in filters),
                mod_files
            )
        return mod_files

    @staticmethod
    def from_json(ref_file: str) -> ModuleBuilder:
        """
        Reads file and creates a module builder
        """
        mod_builder = ModuleBuilder()
        file_path = Path(ref_file)
        mod_builder.set_code(file_path.stem)
        mod_builder.set_url(ref_file)
        return mod_builder

    @staticmethod
    def from_serialized(module_json: dict) -> ModuleBuilder:
        mod_builder = ModuleBuilder()
        mod_builder.set_code(module_json["code"])
        mod_builder.set_url(module_json["url"])
        return mod_builder

    @staticmethod
    def tables_in_module(file_obj: ZipFile | Path, ref_file: str) -> [str]:
        """
        Searches all tables declared in mod.json
        """
        tables: [str] = []
        if isinstance(file_obj, ZipFile):  # Check if given file_obj is zip or not.
            bin_read_mod = file_obj.read(ref_file)
            mod_json = json.loads(bin_read_mod.decode("utf-8"))
        elif isinstance(file_obj, Path):
            with open(file_obj / ref_file, encoding="utf-8") as fl:
                data = fl.read()
                mod_json = json.loads(data)
        else:
            err_msg = "Unknown file_obj type"
            logger.fatal(err_msg)
            raise ValueError(err_msg)
        for table in list(mod_json["tables"].keys()):
            if table[1:] in ("FI", "FootNotes"):
                continue
            tables.append(table[1:].lower().replace("-", "."))
        logger.info(f"Tables found for module --> {tables}")
        return tables

    @staticmethod
    def tables_files_in_module(file_obj: ZipFile | Path, tables: [str]) -> [str]:
        files = []
        if isinstance(file_obj, ZipFile):
            file_list = file_obj.namelist()
        elif isinstance(file_obj, Path):
            file_list = list(
                map(
                    lambda x: str(x).replace(f"{file_obj}/", ""), file_obj.glob("**/*")
                ))
        else:
            err_msg = "Unknown file_obj type"
            logger.fatal(err_msg)
            raise ValueError(err_msg)
        for file in file_list:
            if TablesParser.file_is_table(file) and Path(file).stem in tables:
                files.append(file)
        logger.info(f"Table(s) file(s) found for module --> {files}")
        return files
