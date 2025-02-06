"""
Module with the taxonomy class, that serves to create the 
JSON files with the conversion instructions.

Each time the EBA releases a new taxonomy, the taxonomy_loader.py
module must be run to reflect the changes in the taxonomy.
"""
from pathlib import Path
# from warnings import deprecated
from zipfile import ZipFile


from builders.taxonomy_builder import TaxonomyBuilder
from models.taxonomy import Taxonomy
from parsers.modules_parser import ModulesParser


class TaxonomyParser:

    @staticmethod
    def from_json(input_path: Path) -> Taxonomy:
        """Returns a Taxonomy object from a JSON taxonomy file"""
        tax_builder = TaxonomyBuilder()
        with ZipFile(input_path, mode="r") as zip_file:
            for file in filter(TaxonomyParser.file_is_mod, zip_file.namelist()):
                tax_builder.add_module(ModulesParser.from_json(zip_file, file))
        tax = tax_builder.build()
        if not tax.modules:
            raise TypeError(
                (
                    "No modules found in the taxonomy. "
                    "Please check that the zip file does not contain "
                    "zip files within it"
                )
            )
        return tax

    # @deprecated("Use from_json instead")
    @staticmethod
    def old_from_json(input_path: Path) -> Taxonomy:
        """Returns a Taxonomy object from a JSON taxonomy file"""
        tax_builder = TaxonomyBuilder()
        for module in ModulesParser.old_from_json(input_path):
            tax_builder.add_module(module)
        return tax_builder.build()

    @staticmethod
    def file_is_mod(file_path: str) -> bool:
        return (
            not file_path.startswith("__MACOSX")
            and not ".DS_Store" in file_path
            and "/mod/" in file_path
            and file_path.endswith(".json")
        )
