import json
import logging
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

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
             overwrite: bool = True,
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
            logger.debug(f"Given taxonomy is compressed in a zip file.")
            with ZipFile(tax_path, mode="r") as zip_file:
                mod_files = ModulesParser.filter_files(
                    list(map(lambda x: str(x), zip_file.namelist())),
                    filters
                )
                tax_builder = TaxonomyLoaderServiceHandler.__load(zip_file, mod_files)
        elif tax_path.name.endswith("7z"):
            logger.debug(f"Given taxonomy is compressed in a 7z file.")
            with TemporaryDirectory() as temp_folder:
                # Unzip 7z
                util.unpack_7z(tax_path, Path(temp_folder))
                # Call TaxonomyLoaderService
                TaxonomyLoaderServiceHandler.load(
                    tax_path=list(Path(temp_folder).iterdir())[0],
                    modules_path=modules_path,
                    overwrite=overwrite,
                    filters=filters
                )
            return 0  # Break after this.
        elif tax_path.is_dir():
            logger.debug(f"Given taxonomy is NOT compressed at all.")
            mod_files = ModulesParser.filter_files(
                list(map(
                    # Normalize this mod_files for both UNIX and Windows OS.
                    # UNIX uses "/" and Posix
                    # Windows uses "\" and WindowsPath
                    lambda x: str(x).replace(f"{tax_path.parent}{os.sep}", "").replace("\\", "/"),
                    tax_path.glob("**/*")
                )),
                filters
            )
            tax_builder = TaxonomyLoaderServiceHandler.__load(tax_path, mod_files)
        else:
            logger.fatal(f"Unknown format.")
            logger.info(f"Valid formats are compressed (zip or 7z) or not compressed at all.")
            raise ValueError(f"Unknown taxonomy format")

        # TODO: clean memory
        tax = tax_builder.build()

        # serialize model to file(s)
        map_builder: DimDomMapBuilder = DimDomMapParser.from_json(tax_path)
        if overwrite:
            dim_dom_map = map_builder.build()
        else:
            with open(modules_path / "dim_dom_mapping.json") as fl:
                map_json = json.load(fl)
            old_map_builder = DimDomMapParser.from_serialized(map_json)
            old_map_builder.merge_map(map_builder.build().map)
            dim_dom_map = old_map_builder.build()
        DimDomMapSerializer.to_json(
            modules_path,
            dim_dom_map
        )

        if overwrite:
            mods_index = tax.get_modules_index()
        else:
            with (open(modules_path / "index.json", "r", encoding="utf-8") as fl):
                mods_index = json.load(fl) | tax.get_modules_index()
        ModulesIndexSerializer.to_json(
            modules_path,
            mods_index
        )
        for module in tax.modules:
            ModuleSerializer.to_json(
                modules_path,
                module
            )

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
