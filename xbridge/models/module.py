from models.table import Table
from models.variable import Variable


class Module:
    """Class representing an XBRL Module.

    It has attributes like code, url, taxonomy_code, date, tables
    and input_path, whose main function is to operate with the module and return properties like a specific table from
    the JSON file used as input, an object, a dictionary using the attributes as keys, a module object from a part of
    preprocessed JSON file and the variables that are present in it.

    It is used when taxonomies are loaded to collect the information associated to the tables belonging to the module.

    :param code: The code of the XBRL module.

    :param url: The module reference within the taxonomy.

    :param taxonomy_code: The code of the module within to the taxonomy.

    :param date: Dates contained in the module.

    :param tables: The tables that form the module.

    """

    def __init__(self, code: str=None, url: str=None, taxonomy_code: str=None, date: str=None, tables=None):
        self.__code: str = code
        self.__url: str = url
        self.__taxonomy_code: str = taxonomy_code
        self.__date: str = date
        self.__tables: [Table] = tables if tables is not None else []
        self.__taxonomy_module_path: str = ""

    @property
    def code(self):
        return self.__code

    @property
    def url(self):
        return self.__url

    @property
    def taxonomy_code(self):
        return self.__taxonomy_code

    @property
    def date(self):
        return self.__date

    @property
    def tables(self) -> [Table]:
        return self.__tables.copy()

    @property
    def taxonomy_module_path(self):
        return self.__taxonomy_module_path

    @taxonomy_module_path.setter
    def taxonomy_module_path(self, path: str):
        self.__taxonomy_module_path: str = path

    @property
    def variables_location(self):
        """Returns a dictionary with the :obj:`variables <xbridge.taxonomy.Variable>`
        and the :obj:`tables <xbridge.taxonomy.Table>` where they are present"""
        variables = {}
        for table in self.tables:
            for variable in table.variables:
                if variable.code not in variables:
                    variables[variable.code] = [table.code]
                else:
                    variables[variable.code].append(table.code)
        return variables

    @property
    def repeated_variables(self):
        """Returns a dictionary with the :obj:`variables <xbridge.taxonomy.Variable>` and the :obj:`tables <xbridge.taxonomy.Table>`
        where they are present, if they are repeated"""
        result = {}
        for k, v in self.variables_location.items():
            if len(v) > 1:
                result[k] = v
        return result

    def get_table(self, table_code: str):
        for table in self.tables:
            if table.code == table_code:
                return table
        raise ValueError(f"Table {table_code} not found in module {self.code}")

    def get_variables(self):
        variables: [Variable] = []
        for table in self.tables:
            variables.append(table.variables)
        return variables

    def to_dict(self):
        return {
            "code": self.code,
            "url": self.url,
            "taxonomy_code": self.taxonomy_code,
            "date": self.date,
            "tables": [tab.to_dict() for tab in self.tables],
        }

    def __repr__(self) -> str:
        return f"<Module - {self.code}>"

    def __eq__(self, other):
        if not isinstance(other, Module):
            return NotImplemented
        return (
            self.code == other.code
            and self.url == other.url
            and self.taxonomy_code == other.taxonomy_code
            and self.date == other.date
            and self.taxonomy_module_path == other.taxonomy_module_path
            and len(self.tables) == len(other.tables)
        )