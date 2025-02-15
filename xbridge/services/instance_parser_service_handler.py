import json
from pathlib import Path

from builders.table_builder import TableBuilder
from builders.variable_builder import VariableBuilder
from parsers.dim_dom_map_parser import DimDomMapParser
from parsers.instance_parser import InstanceParser
from parsers.modules_parser import ModulesParser
from serializers.instance_serializer import InstanceSerializer


class InstanceParserServiceHandler:

    @staticmethod
    def parse(input_path: str | Path,
              modules_path: str | Path,
              output_path: str | Path):
        input_path = input_path if isinstance(input_path, Path) \
            else Path(input_path)
        modules_path = modules_path if isinstance(modules_path, Path) \
            else Path(modules_path)
        output_path = output_path if isinstance(output_path, Path) \
            else Path(output_path)

        if not input_path.exists():
            raise FileNotFoundError(f"File {input_path} not found")
        if not modules_path.exists():
            raise FileNotFoundError(f"Modules not found")
        if not (modules_path / "index.json").exists():
            raise FileNotFoundError(f"Modules index not found")
        if not output_path.exists():
            raise ValueError(f"Output directory {output_path} does not exists")

        # Parse instance file
        instance_builder = InstanceParser.from_xml(input_path)
        instance = instance_builder.build()

        # Load module
        module_ref = instance.module_ref
        with open(modules_path / "index.json", "r", encoding="utf-8") as fl:
            index = json.load(fl)

        if module_ref not in index.keys():
            raise ValueError(
                f"Module reference {module_ref} not found"
            )
        else:
            # TODO: load module from serialized
            with open(modules_path / index[module_ref]) as fl:
                module_json = json.load(fl)

            module_builder = ModulesParser.from_serialized(module_json)
            for table_json in module_json.pop("tables"):
                table_builder = TableBuilder()
                table_builder.from_json(table_json)
                # open keys
                # for open_key in table_json.pop("open_keys"):
                #     table_builder.add_open_key(open_key)
                # variables
                for variable_json in table_json.pop("variables"):
                    variable_builder = VariableBuilder()
                    variable_builder.from_json(variable_json)
                    table_builder.add_variable(variable_builder.build())
                # attributes
                # for attribute in table_json.pop("attributes"):
                #     table_builder.add_attribute(attribute)
                module_builder.add_table(table_builder.build())
            module = module_builder.build()
        if module is None:
            raise ValueError("Instance module not found")
        # Load DimDomMap
        with open(modules_path / "dim_dom_mapping.json") as fl:
            map_json = json.load(fl)
        map_builder = DimDomMapParser.from_serialized(map_json)
        # Save file
        InstanceSerializer.to_csv_dpm_1_0(output_path / input_path.stem,
                                          module,
                                          map_builder.build(),
                                          instance)
