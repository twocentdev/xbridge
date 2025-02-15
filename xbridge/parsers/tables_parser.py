import json
from pathlib import Path
from zipfile import ZipFile

from builders.table_builder import TableBuilder
from parsers.variables_parser import VariablesParser


class TablesParser:

    @staticmethod
    def __extract_columns(json_template) -> list:
        columns = []
        for column_code, setup in json_template.items():
            variable_id = setup["eba:documentation"]["KeyVariableID"] if \
                "KeyVariableID" in setup["eba:documentation"] else \
                setup["eba:documentation"]["FactVariableID"]
            col_setup = {
                "code": column_code,
                "variable_id": variable_id,
            }
            if "dimensions" in setup:
                col_setup["dimensions"] = setup["dimensions"]
            columns.append(col_setup)
        return columns

    @staticmethod
    def __extract_datapoints(json_template) -> list:
        datapoints = []
        for elto_k, elto_v in json_template.items():
            datapoint = VariablesParser.from_json(elto_k, elto_v)
            datapoints.append(datapoint)
        return datapoints

    @staticmethod
    def __extract_table_architecture(table_json) -> str:
        """
        This method expects a dict from the table definicion json file. Path should be tableTemplates[0]/obj[0]
        """
        if "datapoint" in table_json.keys():
            return "datapoints"
        else:
            return "headers"

    @staticmethod
    def file_is_table(file_path: str) -> bool:
        """
        Checks if file is a table
        """
        return (
                not file_path.startswith("__MACOSX")
                and not ".DS_Store" in file_path
                and "/tab/" in file_path
                and file_path.endswith(".json")
        )

    @staticmethod
    def from_json(zip_file: ZipFile, ref_file: str) -> TableBuilder:
        bin_read_table = zip_file.read(ref_file)
        table_json = json.loads(bin_read_table.decode("utf-8"))

        tab_builder = TableBuilder()

        # Can parse table ONLY if there is 1 table template
        if len(table_json["tableTemplates"].keys()) > 1:
            raise ValueError(f"More than one table template found in {ref_file}")

        table_code = list(table_json["tableTemplates"].keys())[0]
        tab_builder.set_code(table_code)
        architecture = TablesParser.__extract_table_architecture(table_json["tableTemplates"][table_code]["columns"])
        tab_builder.set_architecture(architecture)
        tab_builder.set_url(f"{Path(ref_file).stem}.csv")
        tab_builder.create_open_keys(table_json["tableTemplates"][table_code])

        if architecture == "datapoints":
            for datapoint in TablesParser.__extract_datapoints(
                    table_json["tableTemplates"][table_code]["columns"]["datapoint"]["propertyGroups"]):
                tab_builder.add_variable(datapoint)
        elif architecture == 'headers':
            for column in TablesParser.__extract_columns(table_json["tableTemplates"][table_code]["columns"]):
                tab_builder.add_column(column)

        return tab_builder
