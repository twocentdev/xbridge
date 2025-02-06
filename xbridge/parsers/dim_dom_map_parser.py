import sys
from pathlib import Path
from zipfile import ZipFile

from lxml import etree
from builders.dim_dom_map_builder import DimDomMapBuilder


class DimDomMapParser:
    __DIM_DOM_MAP_FILE = "www.eba.europa.eu\\eu\\fr\\xbrl\\crr\\dict\\dim\\dim-def.xml"

    @staticmethod
    def from_json(input_path: Path):
        with ZipFile(input_path, mode="r") as zip_file:
            map_builder = DimDomMapBuilder()
            for f in filter(DimDomMapParser.is_dim_def, zip_file.namelist()):
                bin_read = zip_file.read(f)
                try:
                    root = etree.fromstring(
                        bytes(bin_read.decode("utf-8"), encoding="utf-8")
                    )
                except:
                    raise IOError(f"Error while reading dim-dom-map: {f}")
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
            return map_builder.build()

    @staticmethod
    def is_dim_def(file_path: str):
        return (
                not file_path.startswith("__MACOSX")
                and not ".DS_Store" in file_path
                and file_path.endswith("dim-def.xml")
        )
