import json
from zipfile import ZipFile

from builders.table_builder import TableBuilder
from parsers.variables_parser import VariablesParser


class TablesParser:

    @staticmethod
    def file_is_table(file_path: str) -> bool:
        '''
        Checks if file is a table
        '''
        return (
                not file_path.startswith("__MACOSX")
                and not ".DS_Store" in file_path
                and "/tab/" in file_path
                and file_path.endswith(".json")
        )

    @staticmethod
    def from_json(zip_file: ZipFile, ref_file: str, table_ref: str) -> TableBuilder:
        bin_read_table = zip_file.read(ref_file)
        table_json = json.loads(bin_read_table.decode("utf-8"))

        tab_builder = TableBuilder()
        table_code = list(table_json["tableTemplates"].keys())[0]
        tab_builder.set_code(table_code)
        tab_builder.set_url(table_ref + ".csv")
        tab_builder.set_table_zip_path(ref_file)


        for column_name in table_json["tableTemplates"][table_code]\
                .get("columns", []):
            if column_name == "unit":
                tab_builder.add_attribute(column_name)
            elif column_name not in ("datapoint", "factValue"):
                tab_builder.add_open_key(column_name)

        vars_json = {}
        if "datapoint" in table_json["tableTemplates"][table_code]["columns"].keys(): # Check this for DPM 2.0
            vars_json = table_json["tableTemplates"][table_code]["columns"]["datapoint"].get("propertyGroups", [])
        else:
            vars_json = table_json["tableTemplates"][table_code].get("columns", [])
        # vars_json = table_json["tableTemplates"][table_code]["columns"]["datapoint"].get("propertyGroups", [])
        for k, v in vars_json.items():
            tab_builder.add_variable(VariablesParser.from_json(k, v))

        return tab_builder
