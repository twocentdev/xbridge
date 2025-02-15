import copy

import pandas as pd

from models.table import Table
from models.variable import Variable


class TableBuilder:

    def __init__(self):
        self.__table_zip_path: str = ""  # TODO: May fall from here. To builders?
        self.__code: str = ""
        self.__url: str = ""
        self.__open_keys: list = []
        self.__variables: [Variable] = []
        self.__attributes: list = []
        self.__datapoint_df = None

    def set_table_zip_path(self, zip_path: str):
        self.__table_zip_path = zip_path

    def set_code(self, code: str):
        self.__code = code

    def set_url(self, url: str):
        self.__url = url

    def add_open_key(self, key):
        self.__open_keys.append(key)

    def add_variable(self, variable: Variable):
        self.__variables.append(variable)

    def add_attribute(self, attribute):
        self.__attributes.append(attribute)

    def set_datapoint_df(self, df):
        self.__datapoint_df = df

    def from_json(self, json: dict):
        self.set_code(json["code"])
        self.set_url(json["url"])
        # open keys
        for open_key in json.pop("open_keys"):
            self.add_open_key(open_key)
        # attributes
        for attribute in json.pop("attributes"):
            self.add_attribute(attribute)

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
                     self.__table_zip_path,
                     self.__datapoint_df)
