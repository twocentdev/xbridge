from builders.fact_builder import FactBuilder
from models.fact import Fact


class FactParser:

    @staticmethod
    def from_xml(root_elem) -> Fact:
        builder = FactBuilder()
        builder.set_metric(root_elem.tag)
        builder.set_value(root_elem.text)
        builder.set_decimals(root_elem.attrib.get("decimals"))
        builder.set_context(root_elem.attrib.get("contextRef"))
        builder.set_unit(root_elem.attrib.get("unitRef"))
        return builder.build()
