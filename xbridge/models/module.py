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

    :param tables: The tables that form the module.

    """

    def __init__(self,
                 code: str=None,
                 url: str=None,
                 tables=None,
                 taxonomy_architecture: str=None,
                 framework_code: str=None,
                 framework_version: str=None):
        self.__code: str = code
        self.__url: str = url
        self.__tables: [Table] = tables if tables is not None else []
        self.__taxonomy_architecture = taxonomy_architecture
        self.__framework_code = framework_code
        self.__framework_version = framework_version

    @property
    def code(self):
        return self.__code

    @property
    def url(self):
        return self.__url

    @property
    def tables(self) -> [Table]:
        return self.__tables.copy()

    @property
    def taxonomy_architecture(self):
        return self.__taxonomy_architecture

    @property
    def framework_code(self):
        return self.__framework_code

    @property
    def framework_version(self):
        return self.framework_version

    @property
    def variables_location(self):
        """
        Returns a dictionary with the :obj:`variables <xbridge.taxonomy.Variable>`
        and the :obj:`tables <xbridge.taxonomy.Table>` where they are present
        """
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
        """
        Returns a dictionary with the :obj:`variables <xbridge.taxonomy.Variable>`
        and the :obj:`tables <xbridge.taxonomy.Table>` where they are present, if they are repeated
        """
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
        # TODO: update to parse mappers to json
        return {
            "code": self.code,
            "url": self.url,
            "tables": [tab.to_dict() for tab in self.tables],
        }

    def __repr__(self) -> str:
        return f"<Module - {self.code}>"
