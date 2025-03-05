import json
from pathlib import Path

from builders.filing_indicator_builder import FilingIndicatorBuilder

# TODO: this may be a param or config
fil_ind_map_file: Path = Path(__file__).parent.parent / "modules" / \
                     "fil_ind_map.json"


class FilingIndicatorsParser:

    __fil_ind_map = {}

    @classmethod
    def fil_ind_map(cls, filename):
        filename: Path = filename if isinstance(filename, Path) else Path(filename)
        if not cls.__fil_ind_map:
            with open(filename) as fl:
                cls.__fil_ind_map = json.load(fl)
        return cls.__fil_ind_map

    @staticmethod
    def from_xml(root_elem) -> FilingIndicatorBuilder:
        """Parse the XML node with the filing indicator."""

        builder = FilingIndicatorBuilder()
        value = root_elem.attrib.get(
            "{http://www.eurofiling.info/xbrl/ext/filing-indicators}filed"
        )
        if value:
            builder.set_value(True if value == "true" else False)
        else:
            builder.set_value(True)
        fil_ind_map = FilingIndicatorsParser.fil_ind_map(fil_ind_map_file)
        builder.set_table(fil_ind_map.get(root_elem.text, root_elem.text))
        builder.set_context(root_elem.attrib.get("contextRef"))
        return builder
