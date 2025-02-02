import json
from pathlib import Path
from warnings import deprecated
from zipfile import ZipFile

from builders.module_builder import ModuleBuilder
from models.module import Module
from parsers.tables_parser import TablesParser


class ModulesParser:

    @staticmethod
    def file_is_table(file_path: str) -> bool:
        '''
        Checks if file is a table
        '''
        return (
                not file_path.startswith("__MACOSX")
                and not ".DS_Store" in file_path
                and "/tab/" in file_path
                and file_path.endswith(".json")
        )

    @staticmethod
    def from_json(zip_file: ZipFile, ref_file: str):
        """loads one (1) module from the given zip and reference file"""
        mod_builder = ModuleBuilder()
        file_path = Path(ref_file)
        mod_builder.set_code(file_path.stem)
        mod_builder.set_url(ref_file)
        mod_builder.set_taxonomy_code(ref_file.split("/")[7])
        mod_builder.set_date(ref_file.split("/")[8])
        mod_builder.set_taxonomy_module_path(ref_file)

        tables_in_mod = ModulesParser.tables_in_module(zip_file, ref_file)
        for table in filter(ModulesParser.file_is_table, zip_file.namelist()):
            table_name = table.split('/')[-1].split('.json')[0]
            if (table_name in tables_in_mod
                    and ModulesParser.file_is_table(table)): # Could this be redundant??
                mod_builder.add_table(TablesParser.from_json(zip_file, table, table_name))

        return mod_builder.build()

    @deprecated("Use from_json instead")
    @staticmethod
    def old_from_json(input_path: Path = None) -> [Module]:
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
                    for table in TablesParser.old_from_json(zip_file, file_path_obj):
                        mod_builder.add_table(table)
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

    @staticmethod
    def tables_in_module(zip_file: ZipFile, ref_file: str) -> [str]:
        '''
        Searches all tables declared in mod.json
        '''
        tables: [str] = []
        bin_read_mod = zip_file.read(ref_file)
        mod_json = json.loads(bin_read_mod.decode("utf-8"))
        for table in list(mod_json["tables"].keys()):
            tables.append(table[1:].lower().replace("-", "."))
        return tables
