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

    def __init__(self, code=None, url=None, taxonomy_code=None, date=None, tables=None):
        self.__code = code
        self.__url = url
        self.__taxonomy_code = taxonomy_code
        self.__date = date
        self.__tables = tables if tables is not None else []
        self.__taxonomy_module_path = None

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
    def tables(self):
        return self.__tables.copy()

    @property
    def taxonomy_module_path(self):
        return self.__taxonomy_module_path

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

    def get_table(self, table_code):
        for table in self.tables:
            if table.code == table_code:
                return table
        raise ValueError(f"Table {table_code} not found in module {self.code}")

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
