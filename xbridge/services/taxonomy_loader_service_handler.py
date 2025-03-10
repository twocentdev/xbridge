import logging
from pathlib import Path
from zipfile import ZipFile

import others.util
from builders.taxonomy_builder import TaxonomyBuilder
from others import util
from parsers.dim_dom_map_parser import DimDomMapParser
from parsers.modules_parser import ModulesParser
from parsers.tables_parser import TablesParser
from serializers.dim_dom_map_serializer import DimDomMapSerializer
from serializers.module_serializer import ModuleSerializer
from serializers.modules_index_serializer import ModulesIndexSerializer


logger = logging.getLogger(__name__)


class TaxonomyLoaderServiceHandler:

    @staticmethod
    def load(tax_path: str | Path,
             modules_path: str | Path,
             filters: [str] = []):

        logger.info(f"About to load taxonomy {tax_path}")
        tax_path = tax_path if isinstance(tax_path, Path) else Path(tax_path)
        modules_path = modules_path if isinstance(modules_path, Path) else Path(modules_path)

        # taxonomy file exists?
        if not (tax_path.exists() and tax_path.is_file()):
            raise FileNotFoundError(f"File {tax_path} not found or is not a file")
        if not (modules_path.exists() and modules_path.is_dir()):
            raise FileNotFoundError(f"Modules not found.")

        # file is compress??
        if tax_path.name.endswith("zip"):
            logger.info(f"Given taxonomy is compressed in a zip file.")
            with ZipFile(tax_path, mode="r") as zip_file:
                mod_files = ModulesParser.filter_files(
                    list(map(lambda x: str(x), zip_file.namelist())),
                    filters
                )
                tax_builder = TaxonomyLoaderServiceHandler.__load(zip_file, mod_files)
        elif tax_path.name.endswith("7z"):
            logger.info(f"Given taxonomy is compressed in a 7z file.")
        elif tax_path.is_dir():
            logger.info(f"Given taxonomy is NOT compressed at all.")
        else:
            logger.fatal(f"Unknown format.")
            logger.info(f"Valid formats are compressed (zip or 7z) or not compressed at all.")
            raise ValueError(f"Unknown taxonomy format")

        # TODO: if given tax file is 7z, parse to zip
        # if tax_path.suffix not in [".zip", ".7z"]:
        #     raise ValueError("Input file must be a zip or 7z file")
        #
        # parse file(s)
        # with ZipFile(tax_path, mode="r") as zip_file:
        #     tax_builder = TaxonomyBuilder()
        #     mod_files = filter(ModulesParser.file_is_mod, zip_file.namelist())
        #     if len(filtered_paths) > 0:
        #         mod_files = filter(
        #             lambda x: any(x.startswith(base) for base in filtered_paths),
        #             mod_files
        #         )
        #     for file in mod_files:
        #         logger.info(f"New module found in {file}")
        #         module_builder = ModulesParser.from_json(zip_file, file)
        #         # Parsing table(s) file(s)
        #         for table_file in ModulesParser.tables_files_in_module(
        #                 zip_file,
        #                 ModulesParser.tables_in_module(zip_file, file)):
        #             logger.info(f"New table found in {table_file}")
        #             tab_builder = TablesParser.from_json(zip_file, table_file)
        #             module_builder.add_table(tab_builder.build())
        #         tax_builder.add_module(module_builder.build())
        #     tax = tax_builder.build()
        #     # TODO: clean memory
        #
        # dim_dom_map = DimDomMapParser.from_json(tax_path)
        # # serialize model to file(s)
        # DimDomMapSerializer.to_json(
        #     modules_path,
        #     dim_dom_map
        # )
        # ModulesIndexSerializer.to_json(
        #     modules_path,
        #     tax.get_modules_index()
        # )
        # for module in tax.modules:
        #     ModuleSerializer.to_json(
        #         modules_path,
        #         module
        #     )
        # TODO: zip files
        # TODO: delete "temp"/"unzip" files, if necessary

    @staticmethod
    def __load(file_ref: ZipFile | str, mod_files: [str]) -> TaxonomyBuilder:
        tax_builder = TaxonomyBuilder()
        for file in mod_files:
            logger.info(f"New module found in {file}")
            module_builder = ModulesParser.from_json(file)
            # Parsing table(s) file(s)
            for table_file in ModulesParser.tables_files_in_module(
                    file_ref,
                    ModulesParser.tables_in_module(file_ref, file)):
                logger.info(f"New table found in {table_file}")
                tab_builder = TablesParser.from_json(file_ref, table_file)
                module_builder.add_table(tab_builder.build())
            tax_builder.add_module(module_builder.build())
        return tax_builder