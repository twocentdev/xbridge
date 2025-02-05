from pathlib import Path

from parsers.dim_dom_map_parser import DimDomMapParser
from parsers.taxonomies_parser import TaxonomyParser
from serializers.dim_dom_map_serializer import DimDomMapSerializer
from serializers.module_serializer import ModuleSerializer
from serializers.modules_index_serializer import ModulesIndexSerializer


class TaxonomyLoaderServiceHandler:

    @staticmethod
    def load(tax_path: str | Path, modules_path: str | Path) -> None:
        tax_path = tax_path if isinstance(tax_path, Path) \
            else Path(tax_path)
        modules_path = modules_path if isinstance(modules_path, Path) \
            else Path(modules_path)
        # file exists?
        if not tax_path.exists():
            raise FileNotFoundError(f"File {tax_path} not found")
        # file is compress??
        if tax_path.suffix not in [".zip", ".7z"]:
            raise ValueError("Input file must be a zip or 7z file")
        # parse file(s)
        tax = TaxonomyParser.from_json(tax_path)
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
