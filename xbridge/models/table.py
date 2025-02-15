import copy

import pandas as pd


class Table:
    """Class representing an XBRL :obj:`table <xbridge.taxonomy.Table>` as defined in the JSON file.

    Its properties allow to return open keys, variables and attributes from the :obj:`table <xbridge.taxonomy.Table>`. It can also generate a
    variable dataframe or work with one already created.
    Finally, it can return a dictionary using its attributes or a :obj:`Table <xbridge.taxonomy.Table>` object from the preprocessed JSON file.

    It is used when module is loaded to collect the information associated to the variables and open keys
    belonging to the table.

    :param code: The code of the table.

    :param url: The table reference within the module.

    :param open_keys: Open key contained in the table.

    :param variables: the variables that belongs to the table.

    :param attributes: attributes related to the variables that can be extracted from the table.
    """

    def __init__(self,
                 code: str=None,
                 url: str=None,
                 open_keys= [],  # TODO: extract_open_keys in TableBuilder
                 variables= [],  # TODO: extract_variables in TableBuilder
                 attributes= [],
                 architecture: str=None,
                 columns= [],  # TODO: extract_columns in TableBuilder
                 open_keys_map= {} ):
        self.__code = code
        self.__url = url
        self.__open_keys = open_keys if open_keys is not None else []
        self.__variables = variables
        self.__attributes = attributes if attributes is not None else []
        self.__architecture = architecture
        self.__columns = columns
        self.__open_keys_map = open_keys_map

    @property
    def code(self):
        return self.__code

    @property
    def url(self):
        return self.__url

    @property
    def open_keys(self):
        return self.__open_keys.copy()

    @property
    def variables(self):
        return self.__variables.copy()

    @property
    def attributes(self):
        return self.__attributes.copy()

    @property
    def variable_df(self):
        variables = []
        if self.architecture == "datapoints":
            for variable in self.variables:
                variable_info = {}
                for dim_k, dim_v in variable.dimensions.items():
                    if dim_k not in {"unit", "decimals"}:
                        variable_info[dim_k] = dim_v.split(":")[1]
                if "concept" in variable.dimensions:
                    variable_info["metric"] = variable.dimensions["concept"].split(":")[1]
                    del variable_info["concept"]
                variable_info["datapoint"] = variable.code
                variables.append(copy.copy(variable_info))
        elif self.architecture == "headers":
            for column in self.columns:
                variable_info = {"datapoint": column["variable_id"]}
                if "dimensions" in column:
                    for dim_k, dim_v in column["dimensions"].items():
                        if dim_k == "concept":
                            variable_info["metric"] = dim_v.split(":")[1]
                        elif dim_k not in ("unit", "decimals"):
                            variable_info[dim_k.split(":")[1]] = dim_v.split(":")[1]
                variables.append(copy.copy(variable_info))
        return pd.DataFrame(variables)

    @property
    def architecture(self):
        return self.__architecture

    @property
    def columns(self):
        return self.__columns

    @property
    def open_keys_map(self):
        return self.__open_keys_map

    def to_dict(self):
        """Returns a dictionary for the :obj:`table <xbridge.taxonomy.Table>`"""
        dict_ = {
            "code": self.code,
            "url": self.url,
            "architecture": self.architecture,
            "open_keys": self.open_keys
        }
        if self.architecture == "datapoints":
            dict_["variables"] = [var.to_dict() for var in self.variables]
            dict_["attributes"] = self.attributes
        elif self.architecture == "headers":
            dict_["open_keys_mapping"] = self.open_keys_map
            dict_["columns"] = self.columns
        return dict_

    def __repr__(self) -> str:
        return f"<Table - {self.code}>"
