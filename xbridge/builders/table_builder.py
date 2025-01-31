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

    def build(self) -> Table:
        return Table(self.__code, self.__url, self.__open_keys,
                     self.__variables, self.__attributes, self.__table_zip_path)
