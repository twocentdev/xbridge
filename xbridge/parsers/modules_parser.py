import json
from pathlib import Path
from zipfile import ZipFile

from builders.module_builder import ModuleBuilder
from parsers.tables_parser import TablesParser


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
    def from_json(zip_file: ZipFile, ref_file: str) -> ModuleBuilder:
        """loads one (1) module from the given zip and reference file"""
        mod_builder = ModuleBuilder()
        file_path = Path(ref_file)
        mod_builder.set_code(file_path.stem)
        mod_builder.set_url(ref_file)
        mod_builder.set_taxonomy_code(ref_file.split("/")[7])
        mod_builder.set_date(ref_file.split("/")[8])
        mod_builder.set_taxonomy_module_path(ref_file)

        return mod_builder

    @staticmethod
    def tables_in_module(zip_file: ZipFile, ref_file: str) -> [str]:
        '''
        Searches all tables declared in mod.json
        '''
        tables: [str] = []
        bin_read_mod = zip_file.read(ref_file)
        mod_json = json.loads(bin_read_mod.decode("utf-8"))
        for table in list(mod_json["tables"].keys()):
            if table[1:] in ("FI", "FootNotes"):
                continue
            tables.append(table[1:].lower().replace("-", "."))
        return tables

    @staticmethod
    def tables_files_in_module(zip_file: ZipFile, tables: [str]) -> [str]:
        files = []
        for file in zip_file.namelist():
            if TablesParser.file_is_table(file) and Path(file).stem in tables:
                files.append(file)
        return files
