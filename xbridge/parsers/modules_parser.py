import json
import re
from pathlib import Path
from zipfile import ZipFile

from builders.module_builder import ModuleBuilder
from builders.table_builder import TableBuilder
from builders.variable_builder import VariableBuilder
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
        # tax_code = ref_file.split("/")[7]
        mod_builder.set_taxonomy_code(ref_file.split("/")[7])
        # date = ref_file.split("/")[8]
        mod_builder.set_date(ref_file.split("/")[8])
        # if date != "mod":
        #     mod_builder.set_date(date)
        # else:
        #     mod_builder.set_date(tax_code.replace(".", "_"))
        mod_builder.set_taxonomy_module_path(ref_file)

        return mod_builder

    @staticmethod
    def from_serialized(module_json: dict) -> ModuleBuilder:
        mod_builder = ModuleBuilder()
        mod_builder.from_json(module_json)
        #
        # tables = module_json.pop("tables")
        # for table_json in module_json.pop("tables"):
        #     table_builder = TableBuilder()
        #     table_builder.from_json(table_json)
        #     # open keys
        #     for open_key in table_json.pop("open_keys"):
        #         table_builder.add_open_key(open_key)
        #     # variables
        #     for variable_json in table_json.pop("variables"):
        #         variable_builder = VariableBuilder()
        #         variable_builder.from_json(variable_json)
        #         # attributes
        #         for attribute in table_json.pop("attributes"):
        #             table_builder.add_attribute(attribute)
        #
        #         table_builder.add_variable(variable_builder.build())
        #     mod_builder.add_table(table_builder.build())
        #
        return mod_builder

    @staticmethod
    def tables_in_module(zip_file: ZipFile, ref_file: str) -> [str]:
        """
        Searches all tables declared in mod.json
        """
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
