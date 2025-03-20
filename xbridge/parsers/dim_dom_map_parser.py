import logging
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from builders.dim_dom_map_builder import DimDomMapBuilder


logger = logging.getLogger(__name__)


class DimDomMapParser:

    @staticmethod
    def from_json(input_path: Path):
        if input_path.is_file() and input_path.suffix == ".zip":
            logger.debug(f"About to create dim-dom map from zip {input_path}")
            with ZipFile(input_path, mode="r") as zip_file:
                map_builder = DimDomMapBuilder()
                for file in filter(DimDomMapParser.is_dim_def, zip_file.namelist()):
                    logger.debug(f"Dimensions found in {file}")
                    map_builder = DimDomMapParser.__from_json(zip_file, file, map_builder)
        elif input_path.is_dir():
            logger.debug(f"About to create dim-dom map from unzip {input_path}")
            map_builder = DimDomMapBuilder()
            for file in filter(
                    DimDomMapParser.is_dim_def,
                    list(map( lambda x: str(x), input_path.glob("**/*")))
            ):
                logger.debug(f"Dimensions found in {file}")
                map_builder = DimDomMapParser.__from_json(input_path, file, map_builder)
        else:
            err_msg = "Unknown input_path format."
            logger.error(err_msg)
            raise ValueError(err_msg)
        return map_builder

    @staticmethod
    def __from_json(file_obj: ZipFile | Path, file_ref: Path, map_builder: DimDomMapBuilder):
        if isinstance(file_obj, ZipFile):
            bin_read = file_obj.read(file_ref)
            try:
                root = etree.fromstring(
                    bytes(bin_read.decode("utf-8"), encoding="utf-8")
                )
            except:
                raise IOError(f"Error while reading dim-dom-map: {file_ref}")
        elif isinstance(file_obj, Path):
            root = etree.parse(file_obj / file_ref).getroot()
        else:
            err_msg = f"Unknown file_obj type"
            logger.error(err_msg)
            raise ValueError(err_msg)

        ns = {
            'link': 'http://www.xbrl.org/2003/linkbase',
            'xlink': 'http://www.w3.org/1999/xlink'}
        arcroles = root.xpath(
            '//link:definitionArc[@xlink:arcrole="'
            'http://xbrl.org/int/dim/arcrole/dimension-domain"]',
            namespaces=ns)
        for element in arcroles:
            dim_locator = element.get("{%s}from" % (ns["xlink"]))
            dim = root.xpath(
                f'//link:loc[@xlink:label = "{dim_locator}"]',
                namespaces=ns)[0]
            dim = dim.get("{%s}href" % (ns["xlink"])) \
                .split("#")[1].split("_")[1]
            dom_locator = element.get("{%s}to" % (ns["xlink"]))
            dom = root.xpath(f'//link:loc[@xlink:label = "'
                             f'{dom_locator}"]', namespaces=ns)[0]
            dom = dom.get("{%s}href" % (ns["xlink"])).split("#")[1]
            map_builder.add_dom_for_dim(dim, dom)
        return map_builder

    @staticmethod
    def from_serialized(map_json: dict) -> DimDomMapBuilder:
        map_builder = DimDomMapBuilder()
        for dim, dom in map_json.items():
            map_builder.add_dom_for_dim(dim, dom)
        return map_builder

    @staticmethod
    def is_dim_def(file_path: str):
        return (
                not file_path.startswith("__MACOSX")
                and not ".DS_Store" in file_path
                and file_path.endswith("dim-def.xml")
        )
