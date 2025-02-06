from builders.filing_indicator_builder import FilingIndicatorBuilder
from models.filing_indicator import FilingIndicator


class FilingIndicatorsParser:

    @staticmethod
    def from_xml(root_elem) -> FilingIndicator:
        """Parse the XML node with the filing indicator."""

        builder = FilingIndicatorBuilder()
        value = root_elem.attrib.get(
            "{http://www.eurofiling.info/xbrl/ext/filing-indicators}filed"
        )
        if value:
            builder.set_value(True if value == "true" else False)
        else:
            builder.set_value(True)
        builder.set_table(root_elem.text)
        builder.set_context(root_elem.attrib.get("contextRef"))
        return builder.build()
