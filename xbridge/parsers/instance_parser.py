from pathlib import Path

from lxml import etree

from builders.fact_builder import FactBuilder
from builders.instance_builder import InstanceBuilder
from models.fact import Fact
from models.instance import Instance
from parsers.context_parser import ContextParser
from parsers.fact_parser import FactParser
from parsers.filing_indicators_parser import FilingIndicatorsParser


class InstanceParser:

    @staticmethod
    def from_xml(input_path: Path) -> InstanceBuilder:
        root_elem = etree.parse(input_path).getroot()
        builder = InstanceBuilder()
        builder = InstanceParser.__get_units(root_elem, builder)
        builder = InstanceParser.__get_contexts(root_elem, builder)
        builder = InstanceParser.__get_facts(root_elem, builder)
        builder = InstanceParser.__get_module_code(root_elem, builder)
        builder = InstanceParser.__get_filing_indicators(root_elem, builder)
        # What more??
        return builder

    @staticmethod
    def __get_units(root_elem, instance_builder: InstanceBuilder) -> \
            InstanceBuilder:
        units = {}
        for unit in root_elem.findall(
                "{http://www.xbrl.org/2003/instance}unit"):
            unit_name = unit.attrib["id"]
            unit_value = unit.find(
                "{http://www.xbrl.org/2003/instance}measure").text
            ##Workaround
            # We are assuming that currencies always start as iso4217
            if unit_value[:8].lower() == "iso4217:":
                ##Workaround
                # For the XBRL-CSV, we assume one currency for the whole instance
                # We take the first currency we find, because we assume that,
                # in the current EBA architecture, all the facts have the same currency
                # self._base_currency = unit_value
                instance_builder.set_base_currency(unit_value)
                # self._base_currency_unit = unit_name
                instance_builder.set_base_currency_unit(unit_name)
            if unit_value in ["xbrli:pure", "pure"]:
                # self._pure_unit = unit_name
                instance_builder.set_pure_unit(unit_name)
            units[unit_name] = unit_value
        instance_builder.set_units(units)
        return instance_builder

    @staticmethod
    def __get_contexts(root_elem, instance_builder: InstanceBuilder) -> \
            InstanceBuilder:
        contexts = {}
        namespaces = root_elem.nsmap
        for context in root_elem.findall(
                "{http://www.xbrl.org/2003/instance}context",
                namespaces
        ):
            context_object = ContextParser.from_xml(context)
            contexts[context_object.id] = context_object
        instance_builder.set_contexts(contexts)

        instance_builder.set_identifier_prefix(
            root_elem.find(
                "{http://www.xbrl.org/2003/instance}context", namespaces
            )
            .find("{http://www.xbrl.org/2003/instance}entity")
            .find("{http://www.xbrl.org/2003/instance}identifier")
            .attrib.get("scheme")
        )
        return instance_builder

    @staticmethod
    def __get_facts(root_elem, instance_builder: InstanceBuilder) -> \
            InstanceBuilder:
        facts = []
        for child in root_elem:
            facts_prefixes = list(root_elem.nsmap.keys())[
                list(root_elem.nsmap.values()).index(
                    "http://www.eba.europa.eu/xbrl/crr/dict/met"
                )
            ]
            if child.prefix == facts_prefixes:
                fact: Fact = FactParser.from_xml(child)
                instance: Instance = instance_builder.build() # TODO: do not do this
                if fact.unit == instance.base_currency_unit:
                    instance_builder.add_decimals_monetary_set(fact.decimals)
                if fact.unit == instance.pure_unit:
                    instance_builder.add_decimals_percentage_set(fact.decimals)
                facts.append(fact)

        instance_builder.set_facts(facts)

        # TODO: where to do this??
        # self.get_facts_list_dict()
        # self.to_df()
        return instance_builder

    @staticmethod
    def __get_module_code(root_elem, instance_builder: InstanceBuilder) -> \
            InstanceBuilder:
        for child in root_elem:
            if child.prefix == "link":
                ref = child.attrib["{http://www.w3.org/1999/xlink}href"]
                instance_builder.set_module_ref(ref)
                code = ref.split("/mod/")[1].split(".xsd")[0]
                instance_builder.set_module_code(code)
                break
        return instance_builder

    @staticmethod
    def __get_filing_indicators(root_elem, instance_builder: InstanceBuilder) \
            -> InstanceBuilder:
        filing_indicators = []
        for fil_ind in root_elem\
                .find("{http://www.eurofiling.info/xbrl/ext/filing-indicators}fIndicators")\
                .findall("{http://www.eurofiling.info/xbrl/ext/filing-indicators}filingIndicator"):
            filing_indicators.append(FilingIndicatorsParser.from_xml(fil_ind))
            # filing_indicators.append(FilingIndicator(fil_ind))

        instance_builder.set_filing_indicators(filing_indicators)
        # self._filing_indicators = filing_indicators
        first_fil_ind = filing_indicators[0]
        instance: Instance = instance_builder.build() # TODO: do not do this
        fil_ind_context = instance.contexts[first_fil_ind.context]
        # fil_ind_context = self.contexts[first_fil_ind.context]
        instance_builder.set_entity(fil_ind_context.entity)
        # self._entity = fil_ind_context.entity
        instance_builder.set_period(fil_ind_context.period)
        # self._period = fil_ind_context.period
        return instance_builder
