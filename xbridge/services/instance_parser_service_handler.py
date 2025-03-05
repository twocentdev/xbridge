import json
import logging
from pathlib import Path

from parsers.dim_dom_map_parser import DimDomMapParser
from parsers.instance_parser import InstanceParser
from parsers.modules_parser import ModulesParser
from parsers.tables_parser import TablesParser
from parsers.variables_parser import VariablesParser
from serializers.instance_serializer import InstanceSerializer


logger = logging.getLogger(__name__)


class InstanceParserServiceHandler:
    @staticmethod
    def parse(input_path: str | Path,
              modules_path: str | Path,
              output_path: str | Path):
        logger.info(f"About to parse instance {input_path}.")

        input_path = input_path if isinstance(input_path, Path) \
            else Path(input_path)
        modules_path = modules_path if isinstance(modules_path, Path) \
            else Path(modules_path)
        output_path = output_path if isinstance(output_path, Path) \
            else Path(output_path)

        if not input_path.exists():
            err_msg = f"File {input_path} not found"
            logger.fatal(err_msg)
            raise FileNotFoundError(err_msg)
        if not modules_path.exists():
            err_msg = f"Modules not found"
            raise FileNotFoundError(err_msg)
        if not (modules_path / "index.json").exists():
            err_msg = f"Modules index not found"
            raise FileNotFoundError(err_msg)
        if not output_path.exists():
            err_msg = f"Output directory {output_path} does not exists"
            raise ValueError(err_msg)

        # Parse instance file
        instance_builder = InstanceParser.from_xml(input_path)
        instance = instance_builder.build()

        # Load module
        with open(modules_path / "index.json", "r", encoding="utf-8") as fl:
            index = json.load(fl)

        if instance.module_ref not in index.keys():
            err_msg = f"Module reference {instance.module_ref} not found."
            raise ValueError(err_msg)
        else:
            logger.info(f"Found module ref {instance.module_ref} in "
                         f"{index[instance.module_ref]}.")
            with open(modules_path / index[instance.module_ref]) as fl:
                module_json = json.load(fl)

            module_builder = ModulesParser.from_serialized(module_json)
            for table_json in module_json.pop("tables"):
                table_builder = TablesParser.from_serialized(table_json)
                # variables
                if table_json["architecture"] == 'datapoints':
                    for variable_json in table_json.pop("variables"):
                        variable_builder = VariablesParser.from_serialized(
                            variable_json)
                        table_builder.add_variable(variable_builder.build())
                module_builder.add_table(table_builder.build())
            module = module_builder.build()
            # TODO: clean memory

        if module is None:
            raise ValueError("Instance module not found")

        # Load DimDomMap
        with open(modules_path / "dim_dom_mapping.json") as fl:
            map_json = json.load(fl)
        map_builder = DimDomMapParser.from_serialized(map_json)
        dim_dom_map = map_builder.build()

        # Save file
        InstanceSerializer.to_csv(output_path / input_path.stem,
                                  module,
                                  map_builder.build(),
                                  instance)
