import json
import logging
from pathlib import Path

from lxml import etree

from builders.context_builder import ContextBuilder
from builders.instance_builder import InstanceBuilder
from models.fact import Fact
from parsers.context_parser import ContextParser
from parsers.fact_parser import FactParser
from parsers.filing_indicators_parser import FilingIndicatorsParser


logger = logging.getLogger(__name__)


class InstanceParser:

    @staticmethod
    def from_xml(input_path: Path) -> InstanceBuilder:
        logger.debug(f"About to read XML to parse instance.")
        try:
            root_elem = etree.parse(input_path).getroot()
            builder = InstanceBuilder()
            builder = InstanceParser.__get_units(root_elem, builder)
            builder = InstanceParser.__get_contexts(root_elem, builder)
            builder = InstanceParser.__get_facts(root_elem, builder)
            builder = InstanceParser.__get_module_code(root_elem, builder)
            builder = InstanceParser.__get_filing_indicators(root_elem, builder)
        except etree.XMLSyntaxError:
            raise ValueError("Invalid XML format")
        except Exception as e:
            raise ValueError(f"Error parsing instance: {str(e)}")
        # TODO: What more??
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
                instance_builder.set_base_currency(unit_value)
                instance_builder.set_base_currency_unit(unit_name)
            if unit_value in ["xbrli:pure", "pure"]:
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
            context_builder: ContextBuilder = ContextParser.from_xml(context)
            context_object = context_builder.build()
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

        facts_prefixes = []  # TODO: may extract from here outside for?
        for prefix, ns in root_elem.nsmap.items():
            if "http://www.eba.europa.eu/xbrl/crr/dict/met" in ns \
                    or "http://www.eba.europa.eu/xbrl/crr/dict/dim" in ns:
                facts_prefixes.append(prefix)

        for child in root_elem:
            if child.prefix in facts_prefixes:
                fact: Fact = FactParser.from_xml(child)
                if fact.unit == instance_builder.get_base_currency_unit():
                    instance_builder.add_decimals_monetary_set(fact.decimals)
                if fact.unit == instance_builder.get_pure_unit():
                    instance_builder.add_decimals_percentage_set(fact.decimals)
                facts.append(fact)

        instance_builder.set_facts(facts)

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
        eba_fil_ind = "{http://www.eurofiling.info/xbrl/ext/filing-indicators}fIndicators"
        if root_elem \
            .find(eba_fil_ind):
            logger.info(f"Instance is EBA format.")
            for fil_ind in root_elem \
                    .find(eba_fil_ind) \
                    .findall(
                "{http://www.eurofiling.info/xbrl/ext/filing-indicators}filingIndicator"):
                filing_indicators.append(
                    FilingIndicatorsParser.from_xml(fil_ind).build())
        else:
            logger.warning(f"Instance is NOT EBA format.")
            for fil_ind in root_elem \
                .find("{http://www.bde.es/es/fr/esrs/comun/2008-06-01/preambulo}EstadosReportados") \
                .findall("{http://www.bde.es/es/fr/esrs/comun/2008-06-01/preambulo}CodigoEstado"):
                filing_indicators.append(
                    FilingIndicatorsParser.from_xml(fil_ind).build())

        instance_builder.set_filing_indicators(filing_indicators)
        first_fil_ind = filing_indicators[0]
        fil_ind_context = instance_builder.get_contexts() \
            [first_fil_ind.context]
        instance_builder.set_entity(fil_ind_context.entity)
        instance_builder.set_period(fil_ind_context.period)
        return instance_builder
