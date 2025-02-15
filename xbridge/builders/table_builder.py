import copy

import pandas as pd

from models.table import Table
from models.variable import Variable


class TableBuilder:

    def __init__(self):
        self.__table_zip_path = None
        self.__code = None
        self.__url = None
        self.__open_keys = []
        self.__variables = []
        self.__attributes = None
        self.__input_zip_path = None
        self.__architecture = None
        self.__columns = []
        self.__open_keys_mapping = {}

    def set_table_zip_path(self, path):
        self.__table_zip_path = path

    def set_code(self, code: str):
        self.__code = code

    def set_url(self, url: str):
        self.__url = url

    def set_architecture(self, architecture):
        self.__architecture = architecture

    def add_attribute(self, attribute):
        self.__attributes.append(attribute)

    def add_column(self, column):
        self.__columns.append(column)

    def add_variable(self, variable: Variable):
        self.__variables.append(variable)

    def create_open_keys(self, table_template):
        if self.__architecture == 'datapoints':
            for column_name in table_template.get("columns", []):
                if column_name == "unit":
                    self.__attributes.append(column_name)
                elif column_name not in ("datapoint", "factValue"):
                    self.__open_keys.append(column_name)
        elif self.__architecture == 'headers':
            for dim_id, column_ref in table_template["dimensions"].items():
                dim_code = dim_id.split(":")[1]
                self.__open_keys.append(dim_code)
                self.__open_keys_mapping[dim_code] = column_ref[2:]

    def __create_variable_df(self):
        variables = []
        for variable in self.__variables:
            variable_info = {}
            for dim_k, dim_v in variable.dimensions.items():
                if dim_k not in ("unit", "decimals"):
                    variable_info[dim_k] = dim_v.split(":")[1]
            if "concept" in variable.dimensions:
                variable_info["metric"] = \
                    variable.dimensions["concept"].split(":")[1]
                del variable_info["concept"]

            variable_info["datapoint"] = variable.code
            variables.append(copy.copy(variable_info))
        self.__datapoint_df = pd.DataFrame(variables)

    def build(self) -> Table:
        self.__create_variable_df()
        return Table(self.__code,
                     self.__url,
                     self.__open_keys,
                     self.__variables,
                     self.__attributes,
                     self.__architecture,
                     self.__columns,
                     self.__open_keys_mapping)

    def from_json(self, json: dict):
        self.set_code(json["code"])
        self.set_url(json["url"])
        # open keys
        for open_key in json.pop("open_keys"):
            self.add_open_key(open_key)
        # attributes
        for attribute in json.pop("attributes"):
            self.add_attribute(attribute)
