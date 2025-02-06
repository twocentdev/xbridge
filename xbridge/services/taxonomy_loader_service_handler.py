from pathlib import Path
from zipfile import ZipFile

from pandas.plotting import table

from builders.module_builder import ModuleBuilder
from builders.taxonomy_builder import TaxonomyBuilder
from parsers.dim_dom_map_parser import DimDomMapParser
from parsers.modules_parser import ModulesParser
from parsers.tables_parser import TablesParser
from parsers.taxonomies_parser import TaxonomyParser
from serializers.dim_dom_map_serializer import DimDomMapSerializer
from serializers.module_serializer import ModuleSerializer
from serializers.modules_index_serializer import ModulesIndexSerializer


class TaxonomyLoaderServiceHandler:

    @staticmethod
    def load_dpm_1_0(tax_path: str | Path, modules_path: str | Path) -> None:
        tax_path = tax_path if isinstance(tax_path, Path) \
            else Path(tax_path)
        modules_path = modules_path if isinstance(modules_path, Path) \
            else Path(modules_path)
        # taxonomy file exists?
        if not tax_path.exists():
            raise FileNotFoundError(f"File {tax_path} not found")
        # file is compress??
        if tax_path.suffix not in [".zip", ".7z"]:
            raise ValueError("Input file must be a zip or 7z file")
        # parse file(s)
        with ZipFile(tax_path, mode="r") as zip_file:
            tax_builder = TaxonomyBuilder()
            # Parsing modules files
            for module_file in filter(ModulesParser.file_is_mod, zip_file.namelist()):
                module_builder = ModulesParser.from_json(zip_file, module_file)
                module = module_builder.build()
                tax_builder.add_module(module)
                # Parsing table(s) file(s)
                for table_file in ModulesParser.tables_files_in_module(
                        zip_file,
                        ModulesParser.tables_in_module(zip_file, module_file)):
                    table_builder = TablesParser.from_json(zip_file, table_file, table_file)
                    module_builder.add_table(table_builder.build())

        # tax = TaxonomyParser.from_json(tax_path)
        tax = tax_builder.build()
        dim_dom_map = DimDomMapParser.from_json(tax_path)
        # serialize model to file(s)
        DimDomMapSerializer.to_json(
            modules_path,
            dim_dom_map
        )
        ModulesIndexSerializer.to_json(
            modules_path,
            tax.get_modules_index()
        )
        for module in tax.modules:
            ModuleSerializer.to_json(
                modules_path,
                module
            )
