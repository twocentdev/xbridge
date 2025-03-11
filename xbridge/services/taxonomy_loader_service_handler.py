import logging
from pathlib import Path
from zipfile import ZipFile

import others.util
from builders.dim_dom_map_builder import DimDomMapBuilder
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
        if not (tax_path.exists()):
            err_msg = f"File {tax_path} not found"
            logger.fatal(err_msg)
            raise FileNotFoundError(err_msg)
        if not (modules_path.exists() and modules_path.is_dir()):
            err_msg = f"Modules not found."
            logger.fatal(err_msg)
            raise FileNotFoundError(err_msg)

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
            with ZipFile(util.parse_7to_zip(tax_path), mode="r") as zip_file:
                mod_files = ModulesParser.filter_files(
                    list(map(lambda x: str(x), zip_file.namelist())),
                    filters
                )
                tax_builder = TaxonomyLoaderServiceHandler.__load(zip_file, mod_files)
        elif tax_path.is_dir():
            logger.info(f"Given taxonomy is NOT compressed at all.")
            mod_files = ModulesParser.filter_files(
                list(map(lambda x: str(x).replace(f"{tax_path.parent}/", ""), tax_path.glob("**/*"))),
                filters
            )
            tax_builder = TaxonomyLoaderServiceHandler.__load(tax_path, mod_files)
        else:
            logger.fatal(f"Unknown format.")
            logger.info(f"Valid formats are compressed (zip or 7z) or not compressed at all.")
            raise ValueError(f"Unknown taxonomy format")

        # TODO: if given tax file is 7z, parse to zip
        # if tax_path.suffix not in [".zip", ".7z"]:
        #     raise ValueError("Input file must be a zip or 7z file")
        #
        # parse file(s)
        # with ZipFile(tax_path, mode="r") as file_obj:
        #     tax_builder = TaxonomyBuilder()
        #     mod_files = filter(ModulesParser.file_is_mod, file_obj.namelist())
        #     if len(filtered_paths) > 0:
        #         mod_files = filter(
        #             lambda x: any(x.startswith(base) for base in filtered_paths),
        #             mod_files
        #         )
        #     for file in mod_files:
        #         logger.info(f"New module found in {file}")
        #         module_builder = ModulesParser.from_json(file_obj, file)
        #         # Parsing table(s) file(s)
        #         for table_file in ModulesParser.tables_files_in_module(
        #                 file_obj,
        #                 ModulesParser.tables_in_module(file_obj, file)):
        #             logger.info(f"New table found in {table_file}")
        #             tab_builder = TablesParser.from_json(file_obj, table_file)
        #             module_builder.add_table(tab_builder.build())
        #         tax_builder.add_module(module_builder.build())
        #     tax = tax_builder.build()
        #     # TODO: clean memory
        #
        tax = tax_builder.build()

        map_builder: DimDomMapBuilder = DimDomMapParser.from_json(tax_path)
        # serialize model to file(s)
        DimDomMapSerializer.to_json(
            modules_path,
            map_builder.build()
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
        # TODO: zip files
        # TODO: delete "temp"/"unzip" files, if necessary

    @staticmethod
    def __load(file_ref: ZipFile | Path, mod_files: [str]) -> TaxonomyBuilder:
        tax_builder = TaxonomyBuilder()
        file_ref = file_ref.parent if isinstance(file_ref, Path) else file_ref
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