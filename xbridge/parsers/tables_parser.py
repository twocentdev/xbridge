import json
from pathlib import Path
from warnings import deprecated
from zipfile import ZipFile

from builders.table_builder import TableBuilder
from builders.variable_builder import VariableBuilder
from models.table import Table
from parsers.variables_parser import VariablesParser


class TablesParser:

    @staticmethod
    def from_json(zip_file: ZipFile, ref_file: str, table_ref: str):
        # print(f"About to process {table_ref} in {ref_file}")
        bin_read_table = zip_file.read(ref_file)
        table_json = json.loads(bin_read_table.decode("utf-8"))

        tab_builder = TableBuilder()
        table_code = list(table_json["tableTemplates"].keys())[0]
        tab_builder.set_code(table_code)
        tab_builder.set_url(table_ref + ".csv")
        tab_builder.set_table_zip_path(ref_file)

        for column_name in table_json["tableTemplates"][table_code].get("columns", []):
            if column_name == "unit":
                tab_builder.add_attribute(column_name)
            elif column_name not in ("datapoint", "factValue"):
                tab_builder.add_open_key(column_name)

        vars_json = table_json["tableTemplates"][table_code]["columns"]["datapoint"].get("propertyGroups", [])
        for k, v in vars_json.items():
            # print(f"Found variable {k}")
            tab_builder.add_variable(VariablesParser.from_json(k, v))

        return tab_builder.build()

    @deprecated("Use from_json instead")
    @staticmethod
    def old_from_json(zip_file: ZipFile, input_path: Path):
        """Extracts the :obj:`tables <xbridge.taxonomy.Table>` in the JSON files for the :obj:`modules <xbridge.taxonomy.Module>` in the taxonomy"""
        tables: [Table] = []

        bin_read_mod = zip_file.read(str(input_path))
        info = json.loads(bin_read_mod.decode("utf-8"))

        for table_code, table in info["tables"].items():
            if table_code[1:] in ("FI", "FootNotes"):
                continue

            table_url = table["url"]
            table_folder_name = table_code[1:].lower().replace("-", ".")
            # table_folder_name = table_folder_name.replace("-", ".")

            path = str(input_path).split("/mod/")[0]

            table_path = (
                path + "/tab/" + table_folder_name + "/" + table_folder_name + ".json"
            )
            # table = Table.from_taxonomy(
            #     zip_file, table_path, code=table_code[1:], url=table_url
            # )
            tab_builder = TableBuilder()
            tab_builder.set_code(table_code[1:])
            tab_builder.set_url(table_url)
            tab_builder.set_table_zip_path(table_path)

            # obj = cls(code=code, url=url)
            # obj.table_zip_path = table_path
#
            # obj.extract_open_keys(zip_file)
            # open_keys = []
            # attributes = []

            bin_read_table = zip_file.read(table_path)

            table_json = json.loads(bin_read_table.decode("utf-8"))
            table_template = table_json["tableTemplates"][table_code[1:]]
            for column_name in table_template.get("columns", []):
                if column_name == "unit":
                    # attributes.append(column_name)
                    tab_builder.add_attribute(column_name)
                elif column_name not in ("datapoint", "factValue"):
                    # open_keys.append(column_name)
                    tab_builder.add_open_key(column_name)

            # obj.extract_variables(zip_file)
            # variables: [Variable] = []
            # self._variables = []
            # bin_read_variables = zip_file.read(self.table_zip_path)

           # table_json = json.loads(bin_read.decode("utf-8"))
            if table_code[1:] in table_json["tableTemplates"]:
                variables_dict = table_json["tableTemplates"][table_code[1:]]["columns"][
                    "datapoint"
                ]["propertyGroups"]
                for elto_k, elto_v in variables_dict.items():
                    # datapoint = Variable.from_taxonomy(elto_k, elto_v)
                    var_builder = VariableBuilder()
                    var_builder.set_code(elto_k)
                    var_builder.set_dimensions(elto_v["dimensions"])
                    if "decimals" in elto_v:
                        var_builder.set_attributes(elto_v["decimals"])
                    # obj = cls(code=variable_id)
                    # obj.extract_dimensions(variable_dict)
                    # return obj
                    tab_builder.add_variable(var_builder.build())

            tables.append(tab_builder.build())
        return tables