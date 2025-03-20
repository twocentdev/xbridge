import csv
import json
from pathlib import Path

from builders.filing_indicator_builder import FilingIndicatorBuilder
from others.app_config import AppConfig

# TODO: this may be a param or config
fil_ind_map_file: Path = Path(__file__).parent.parent.parent / "res" / "fil_ind_map.csv"


class FilingIndicatorsParser:

    __fil_ind_map = {}

    @classmethod
    def fil_ind_map(cls):
        app_config = AppConfig()
        if not cls.__fil_ind_map:
            with (open(app_config.get_value("filing_indicators"), newline="")
                  as
                  csv_file):
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    k = row[0]
                    v = row[1]
                    cls.__fil_ind_map[0] = 1
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
        fil_ind_map = FilingIndicatorsParser.fil_ind_map()
        builder.set_table(fil_ind_map.get(root_elem.text, root_elem.text))
        builder.set_context(root_elem.attrib.get("contextRef"))
        return builder
