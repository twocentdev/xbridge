from builders.context_builder import ContextBuilder
from builders.scenario_builder import ScenarioBuilder
from models.context import Context
from parsers.scenario_parser import ScenarioParser


class ContextParser:

    @staticmethod
    def from_xml(root_elem) -> Context:
        builder = ContextBuilder()
        builder.set_id(root_elem.attrib["id"])
        builder.set_entity(
            root_elem.find("{http://www.xbrl.org/2003/instance}entity")
            .find("{http://www.xbrl.org/2003/instance}identifier")
            .text
        )
        builder.set_period(
            root_elem.find("{http://www.xbrl.org/2003/instance}period")
            .find("{http://www.xbrl.org/2003/instance}instant")
            .text
        )
        builder.set_scenario(ScenarioParser.from_xml(
            root_elem.find("{http://www.xbrl.org/2003/instance}scenario")
        ))
        return builder.build()
