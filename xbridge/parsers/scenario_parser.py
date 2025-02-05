from builders.scenario_builder import ScenarioBuilder
from models.scenario import Scenario


class ScenarioParser:

    @staticmethod
    def from_xml(root_elem) -> Scenario:
        builder = ScenarioBuilder()
        if root_elem is not None:
            for child in root_elem:
                ##Workaround
                # We are dropping the prefixes of the dimensions and the members
                # lxml is not able to work with namespaces in the values of the attributes
                # or the items.
                # On the other hand, we know that there are no potential conflicts because
                # the EBA is not using external properties, and for one property all the
                # items are owned by the same entity.
                dimension = child.attrib["dimension"].split(":")[1]
                # value = None
                if child.getchildren():
                    value = child.getchildren()[0].text
                else:
                    value = child.text
                value = value.split(":")[1] if ":" in value else value
                # self.dimensions[dimension] = value
                builder.set_dimension(dimension, value)
                return builder.build()
